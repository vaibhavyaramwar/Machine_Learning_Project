from debugpy import configure
from housing.config.configuration import Configuration
from housing.exception import HousingException
from housing.pipeline.pipeline import Pipeline
from housing.logger import logging

def main():

    try:
        #pipeline = Pipeline()
        #pipeline.run_pipeline()

        configuration = Configuration()
        info = configuration.get_data_transformation_config()  
        print(info)      

    except Exception as e:
        print(e)
        logging.error(f"Exception in processing of pipeline : {e}")


if __name__ == "__main__":
    main()

