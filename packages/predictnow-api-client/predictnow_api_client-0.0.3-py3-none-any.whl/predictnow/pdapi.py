# use command: pip install -e .
# to install and test it locally before you publish it
import json
import os
from zipfile import ZipFile

import pandas as pd
from predictnow import cert

from .notifier import MLTrainingCompletedNotifier
from uuid import uuid4
from typing import Dict
import requests

# TODO: change the host url to Apigee
# host_api = should call proxy API gee //authentication/authorization
# host = "http://127.0.0.1:8080"
import firebase_admin
from firebase_admin import credentials

from .predict_result import PredictResult
from .training_result import TrainingResult


class PredictNowClient:
    def __init__(self, url, api_key):
        self.api_key = api_key
        self.host = url
        cred = credentials.Certificate(cert)
        if len(firebase_admin._apps) == 0:  # check if firebase is already init
            firebase_admin.initialize_app(cred)

    def train(self, input_path, params: Dict[str, str]) -> TrainingResult:
        try:
            params['train_id'] = params['train_id'] if "train_id" in params else str(uuid4())
            notifier = MLTrainingCompletedNotifier(
                params['username'], params['train_id'])
            files = {'csv': open(input_path, 'rb')}

            url = self.host + "/trainings"

            response = requests.post(
                url,
                files=files,
                data=params,
                timeout=300,
            )  # prevents TaskCancelled error

            notifier.wait_for_result()

            extract_path = os.path.join(os.getcwd(), "temp")
            os.makedirs(extract_path, exist_ok=True)
            self.save_to_output(
                params={"username": params['username']},
                output_path=extract_path
            )

            return self.deserialize(
                path=extract_path,
                username=params['username'],
                suffix=params['suffix'],
            )
        except:
            return TrainingResult(
                success=False,
                feature_importance=dict(),
                feat_train=dict(),
                feat_test=dict(),
                lab_test=dict(),
                lab_train=dict(),
                performance_metrics=dict(),
                dataframe_train_diff=dict(),
                dataframe_train_undiff=dict(),
                training_parameters=list(),
                predicted_prob_cv=dict(),
                predicted_prob_test=dict(),
                predicted_targets_cv=dict(),
                predicted_targets_test=dict(),
            )

    def predict(self, input_path, params: Dict[str, str]) -> PredictResult:
        files = {'live_file': open(input_path, 'rb')}

        url = self.host + "/predictions"
        response = requests.post(url, data=params, files=files)
        print(response.content)
        response = json.loads(response.content.decode('utf-8'))
        return PredictResult(
            title=response["title"],
            filename=response["filename"],
            objective=response["objective"],
            eda=response["eda"],
            too_many_nulls_list=response["too_many_nulls_list"],
            suffix=response["suffix"],
            labels=response["labels"],
            probabilities=response["probabilities"],
        )

    # TODO Confirm to Radu, what's the difference between save_to_output, download_all_files(path), and DownloadFiles(model_name, path)
    # Save results output for the model named model_name to the local directory specified by output_path
    # The following are downloaded (the .pkl file for the model itself remains on the server):
    #  - performance metrics file
    #  - feature selection chart
    #  - Feature selection importance score csv file
    #  - In-sample and out-of-sample predictions
    def save_to_output(self, params: Dict[str, str], output_path=""):
        output_path = output_path if output_path else os.getcwd()
        url = self.host + "/saveoutput"

        response = requests.post(
            url,
            data=params,
        )
        response = response.content

        file = open(os.path.join(output_path, params["username"] + ".zip"), "wb")
        file.write(response)
        file.close()

        return {
            "success": True,
            "message": "The result " + params["username"] + ".zip has been saved into " + output_path,
        }

    # # TODO if these download files included, we can merge it.
    # # Just give flag to the params, saying 'all:true'
    # def download_all_files(self, params: Dict[str, str] ):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # def download_files(self, params: Dict[str, str]):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # TODO confirm to radu, I think we can merge DeleteAllData and Delete Data.
    # # Just give flag to the params, saying 'all:true'
    # # DeleteAllData: Deletes all input and output files from the current account on the server.
    # # DeleteData(model_name): Deletes input and output files associated with the specified model
    # def delete_data(self, params: Dict[str, str] ):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Sends reset password request link to the current account email.
    # def reset_password(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Sends reset password request link to the current account email.
    # def reset_password(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # #Get the current account status. Available states are unlocked or locked
    # def get_account_status(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Get the current account subscription details, such as start date of payment, next due payment, amount
    # # to be paid.
    # def get_subscription_details(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Return: dictionary whose keys and values are strings. Keys represent method names, and values
    # # represent description of the corresponding method
    # # use dir(self)???
    # def get_all_methods(self):
    #     ...
    #     raise Exception("method is not implemented yet.")

    def deserialize(self, path, username, suffix):
        with ZipFile(os.path.join(path, username + ".zip"), 'r') as zipObj:
            zipObj.extractall(path)

        path = os.path.join(path, username)

        with open(os.path.join(path, "performance_metrics_" + suffix + ".txt")) as f:
            performance_metrics = f.readlines()
            performance_metrics = [i.replace("\n", "") for i in performance_metrics]

        with open(os.path.join(path, "personal_" + suffix + ".json")) as f:
            training_parameters = f.read()
            training_parameters = json.loads(training_parameters)

        csv_files = {
            "dataframe_train_diff_": dict(),
            "dataframe_train_undiff_": dict(),
            "feat_test_": dict(),
            "feat_train_": dict(),
            "feature_importance_": dict(),
            "lab_test_": dict(),
            "lab_train_": dict(),
            "predicted_prob_cv_": dict(),
            "predicted_prob_test_": dict(),
            "predicted_targets_cv_": dict(),
            "predicted_targets_test_": dict(),
        }

        for file_name_prefix in csv_files:
            dataframe = pd.read_parquet(os.path.join(path, file_name_prefix + suffix + ".parquet"))
            csv_files[file_name_prefix] = dataframe

        return TrainingResult(
            success=True,
            feature_importance=csv_files["feature_importance_"],
            feat_train=csv_files["feat_train_"],
            feat_test= csv_files["feat_test_"],
            lab_test= csv_files["lab_test_"],
            lab_train= csv_files["lab_train_"],
            performance_metrics= performance_metrics,
            dataframe_train_diff=csv_files["dataframe_train_diff_"],
            dataframe_train_undiff=csv_files["dataframe_train_undiff_"],
            training_parameters= training_parameters,
            predicted_prob_cv= csv_files["predicted_prob_cv_"],
            predicted_prob_test= csv_files["predicted_prob_test_"],
            predicted_targets_cv= csv_files["predicted_targets_cv_"],
            predicted_targets_test= csv_files["predicted_targets_test_"],
        )
