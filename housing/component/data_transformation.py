from msilib.schema import Class
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact


class DataTransformation:

    def __init__(self,dataTransformationConfig : DataTransformationConfig,
                 dataIngestionArtifact : DataIngestionArtifact,
                 dataValidationArtifact : DataValidationArtifact):
        try:
            self.dataTransformationConfig = dataTransformationConfig
            self.dataIngestionArtifact = dataIngestionArtifact
            self.dataValidationArtifact = dataValidationArtifact
        except Exception as e:
            raise HousingException(e,sys) from e

    




    
