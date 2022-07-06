from cgi import test
from operator import is_
import re
from xmlrpc.client import Boolean
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import sys,os
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd
import json


class DataValidation:
     
    def __init__(self,dataValidationConfig:DataValidationConfig,
                       dataingestionArtifact:DataIngestionArtifact):
          try:
            self.dataValidationConfig = dataValidationConfig
            self.dataingestionArtifact = dataingestionArtifact
          except Exception as e:
            raise HousingException(e,sys) from e

    def is_train_test_file_exists(self) -> Boolean:
        
        try:

            logging.info("Checking Avalability of Training and Test file")
            is_train_file_exists = False
            is_test_file_exists = False

            is_train_file_exists = os.path.exists(self.dataingestionArtifact.train_file_path)
            is_test_file_exists = os.path.exists(self.dataingestionArtifact.test_file_path)

            is_available = is_train_file_exists and is_test_file_exists

            logging.info(f"is train and test file exists? {[is_available]}")


            if not is_available:
                training_file_path = self.dataingestionArtifact.train_file_path
                test_file_path = self.dataingestionArtifact.test_file_path
                message = f"Training File at Path : {training_file_path} or testing file at path : {test_file_path} not exixts"
                logging.info(message)
                raise Exception(message)

            return is_available

        except Exception as e:
            raise HousingException(e,sys) from e        


    def validate_dataset_Schema(self) -> Boolean:
        try:
            
            validation_status = False

            # Validation training and testing dataset using schema file

            # 1 Number of column
            # 2 Check the value of ocean appoximity
            # 3 Check Column names



            validation_status = True
            return validation_status

        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.dataingestionArtifact.train_file_path)
            test_df = pd.read_csv(self.dataingestionArtifact.test_file_path)

            return train_df,test_df

        except Exception as e:
            raise HousingException(e,sys) from e    


    def save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df,test_df = self.get_train_and_test_df()
            profile.calculate(train_df,test_df)
            report = json.loads(profile.json())

            report_file_path = self.dataValidationConfig.report_file_path
            report_dir_name = os.path.dirname(self.dataValidationConfig.report_file_path)
            os.makedirs(report_dir_name,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)

            return report

        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)
            
            report_page_file_path = self.dataValidationConfig.report_page_file_path
            report_page_path_dir_name = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_path_dir_name,exist_ok=True)

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise HousingException(e,sys) from e    


    def is_data_drift_found(self):
        try:

            report = self.save_data_drift_report()
            self.save_data_drift_report_page()

            return True
        except Exception as e:
            raise HousingException(e,sys) from e


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            is_available = self.is_train_test_file_exists()

            if is_available:

                self.validate_dataset_Schema()
                validation_status = self.validate_dataset_Schema()
            
                self.is_data_drift_found()

            dataValidationArtifact = DataValidationArtifact(schema_file_path=self.dataValidationConfig.schema_file_path,
            report_file_path=self.dataValidationConfig.report_file_path,
            report_page_file_path=self.dataValidationConfig.report_page_file_path,
            is_validated=True,
            message="Data Validation perfomred successfully")

            logging.info(f"Data Validation Artifact : {[dataValidationArtifact]}")

        except Exception as e:
            raise HousingException(e,sys) from e
