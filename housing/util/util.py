import yaml
from housing.exception import HousingException
import os,sys
from housing.constant import *
import numpy as np
import pandas as pd
import dill

def read_yaml_file(file_path:str) -> dict:
    """
        Reads a YAML file and returns the contents as dictionary.
        file_path: str 
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e

def load_data(file_path : str, schema_file_path : str) -> pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(file_path=schema_file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataFrame = pd.read_csv(file_path)

        error_message = ""

        for feature in dataFrame.columns:

            print(feature)
            if feature in list(schema.keys()):
                dataFrame[feature].astype(schema[feature])
            else:
                error_message = f"{error_message} \n Column : [{feature} is not in the schema]"

            if len(error_message) > 0:
                raise Exception(error_message)

        return dataFrame

    except Exception as e:
        raise HousingException(e,sys) from e

def save_numpy_array_data(file_path:str,array : np.array):
        """
            save numpy array data to file
            file_path : str location of file to save
            array : np.array data to save
        """
        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path,exist_ok=True)
            with open(file_path,"wb") as file_obj:
                np.save(file_obj,array)
        except Exception as e:
            raise HousingException(e,sys) from e

def load_numpy_array_data(file_path:str) -> np.array:
        """
            load numpy array data from file
            file_path : str location of file to load
            return: np.array data loaded 
        """
        try:
            with open(file_path,"rb") as file_obj:
                return np.load(file_obj)
        except Exception as e:
            raise HousingException(e,sys) from e


def save_obj(file_path:str,obj):
        """
            This function is used tgo save the object at file_path
            file_path : str location of the object to save
            obj : object to save in file path
        """
        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "wb") as file_obj:
                dill.dump(obj, file_obj)    

        except Exception as e:
            raise HousingException(e,sys) from e

def load_object(file_path:str):
        """
            file_path : str
        """
        try:
            with open(file_path,"rb") as file_obj:
                return dill.load(file_obj)
        except Exception as e:
            raise HousingException(e,sys) from e

    