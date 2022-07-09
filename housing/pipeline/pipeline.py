from housing.config.configuration import Configuration
from housing.logger import logging
from housing.exception import HousingException

from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig
import sys,os
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation

class Pipeline:


    def __init__(self,config:Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_ingestion(self) -> DataIngestion:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_validation(self,dataingestionArtifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
          data_validation =  DataValidation(dataValidationConfig = self.config.get_data_validation_config(),
                            dataingestionArtifact=dataingestionArtifact)

          return data_validation.initiate_data_validation()

        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_transformation(self,dataIngestionArtifact:DataIngestionArtifact,
                                       dataValidationArtifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            dataTransformation = DataTransformation(dataTransformationConfig=self.config.get_data_transformation_config(),
            dataIngestionArtifact=dataIngestionArtifact,dataValidationArtifact=dataValidationArtifact)

            dataTransformation.initiate_data_transformation()

        except Exception as e:
            raise HousingException(e,sys) from e

    def start_model_trainer():
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_model_evaluation():
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_model_pusher():
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    def run_pipeline(self):
        try:
            # Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)        
            data_transformation_artifact = self.start_data_transformation(dataIngestionArtifact=data_ingestion_artifact,
                                                                            dataValidationArtifact=data_validation_artifact)
        except Exception as e:
            raise HousingException(e,sys) from e

    