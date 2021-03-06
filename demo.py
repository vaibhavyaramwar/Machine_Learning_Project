from ctypes import util
from debugpy import configure
from housing.config.configuration import Configuration
from housing.constant import ROOT_DIR
from housing.exception import HousingException
from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.util.util import load_data
import os

def main():

    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()

        #configuration = Configuration()
        #info = configuration.get_data_transformation_config()  
        #print(info)
        # 
        #       
        #train_file_path = r"E:\Preparation\iNeuron\Full_Stack_Data_Science\Live_Class_Machine_Learning\ML_Project\ML_Project_Pract\Machine_Learning_Project\housing\artifact\data_ingestion\2022-07-06-17-49-29\ingested_data\train\housing.csv"
        #schema_file_path = os.path.join(ROOT_DIR,"config","schema.yaml")
        #df = load_data(train_file_path,schema_file_path)
        #print(df.columns)
        #print(df.dtypes)

    except Exception as e:
        print(e)
        logging.error(f"Exception in processing of pipeline : {e}")


if __name__ == "__main__":
    main()

