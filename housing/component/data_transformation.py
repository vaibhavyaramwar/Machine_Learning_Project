from msilib.schema import Class
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact
from housing.constant import *
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from housing.util.util import read_yaml_file,load_data,save_obj,save_numpy_array_data

import sys,os

#   longitude: float
#   latitude: float
#   housing_median_age: float
#   total_rooms: float
#   total_bedrooms: float
#   population: float
#   households: float
#   median_income: float
#   median_house_value: float
#   ocean_proximity: category
#   income_cat: float


class FeatureGenerator(BaseEstimator,TransformerMixin):

    def __init__(self,add_bedroom_per_room=True,
                       total_rooms_ix=3,
                       population_ix=5,
                       household_ix=6,
                       total_bedroom_ix=4,columns=None):

        """
            Feature Generator Initiation
            add_bedroom_per_room : bool
            total_rooms_ix : int index number of total room columns
            population_ix : int index number of total population column
            household_ix : int index number of households columns
            total_bedroom_ix : int index number of bedrooms columns
        """

        try:
            self.columns = columns

            if self.columns is not None:
                total_rooms_ix =  self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix =   self.columns.index(COLUMN_POPULATION)   
                household_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedroom_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)
            
            self.add_bedroom_per_room = add_bedroom_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.household_ix = household_ix
            self.total_bedroom_ix = total_bedroom_ix
        except Exception as e:
            raise HousingException(e,sys) from e

    def fit(self,X,y=None):
        return self

    def transform(self,X,y=None):
        try:
            room_per_household = X[:,self.total_rooms_ix] / X[:,self.household_ix]
            population_per_househole = X[:,self.population_ix] / X[:,self.household_ix]

            if self.add_bedroom_per_room:
                bedrooms_per_room = X[:,self.total_bedroom_ix] / X[:,self.total_rooms_ix]
                generated_feature = np.c_[X,room_per_household,population_per_househole,bedrooms_per_room]
            else:
                generated_feature = np.c_[X,room_per_household,population_per_househole]

            return generated_feature
        except Exception as e:
            raise HousingException(e,sys) from e


class DataTransformation:

    def __init__(self,dataTransformationConfig : DataTransformationConfig,
                 dataIngestionArtifact : DataIngestionArtifact,
                 dataValidationArtifact : DataValidationArtifact):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.dataTransformationConfig = dataTransformationConfig
            self.dataIngestionArtifact = dataIngestionArtifact
            self.dataValidationArtifact = dataValidationArtifact
        except Exception as e:
            raise HousingException(e,sys) from e

    
    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.dataValidationArtifact.schema_file_path
            
            dataset_schema = read_yaml_file(schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]

            categotrical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            num_pipeline = Pipeline(steps=[('imputer',SimpleImputer(strategy="median")),
                                            ('feature_generator',FeatureGenerator(add_bedroom_per_room=self.dataTransformationConfig.add_bedroom_per_room,
                                        columns=numerical_columns)),
                                            ('scaler',StandardScaler())
                                    ])

            cat_pipeline = Pipeline(steps=[('imputer',SimpleImputer(strategy="most_frequent")),
                                           ('oneHotEncoder',OneHotEncoder()),
                                           ('scaling',StandardScaler(with_mean=False))
                                    ])

            logging.info(f"Categorical Columns : [{categotrical_columns}]")
            logging.info(f"Numerical Columns : [{numerical_columns}]")
            
            preprocessing = ColumnTransformer([('num_pipeline',num_pipeline,numerical_columns),
                                                ('cat_pipeline',cat_pipeline,categotrical_columns)])


            return preprocessing

        except Exception as e:
            raise HousingException(e,sys) from e

    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            
            logging.info("Obtaining Preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Obtaining training and test file path.")
            train_file_path = self.dataIngestionArtifact.train_file_path
            test_file_path = self.dataIngestionArtifact.test_file_path


            schema_file_path = self.dataValidationArtifact.schema_file_path

            logging.info("Loading training and testing data as Pandas DataFrame")
            train_df = load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path,schema_file_path=schema_file_path)


            schma = read_yaml_file(file_path=schema_file_path)

            target_column_name = schma[TARGET_COLUMN_KEY]

            logging.info("Splitting input and target feature from training and testing dataframe")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)

            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying pre-processing object on training datafreame and testing dataframe")
            logging.info(f"input_feature_train_df : {input_feature_train_df.columns}")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]


            transfomrmed_train_dir = self.dataTransformationConfig.transfomrmed_train_dir
            transformed_test_dir = self.dataTransformationConfig.transformed_test_dir

            train_file_path = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_path = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transfomrmed_train_dir,train_file_path)
            transformed_test_file_path = os.path.join(transformed_test_dir,test_file_path)

            logging.info("saving transformed training and testing array.")
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preproessing_obj_file_path =self.dataTransformationConfig.preprocessed_object_file_path

            logging.info("saving preprocessing object.")
            save_obj(file_path=preproessing_obj_file_path,obj= preprocessing_obj)

            data_transformation_artifact =DataTransformationArtifact(is_transformed=True,
            message="Data Transformation Successful",
            transfomrmed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_object_file_path=preproessing_obj_file_path)

            logging.info(f"Data Transformation Artifact : {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e


