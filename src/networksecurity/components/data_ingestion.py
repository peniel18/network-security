import pymongo.mongo_client
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 
from networksecurity.entity.config_entity import DataIngestionConfig
import os 
import sys
import pymongo 
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from pymongo import Mongo
import pandas as pd
import numpy as np 


load_dotenv()
MONGO_DB_URI = os.getenv("MANGO_DB_URI")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try: 
            self.data_ingestion_config = data_ingestion_config
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def export_collection_as_datafram(self) -> pd.DataFrame:
        """
        Read data from mongo db and export it as pandas dataframe

        Returns:
            pd.DataFrame
        """
        try:
            logging.info(f"export_collection_as_dataframe has started")
            database_name = self.data_ingestion_config.database_name
            collectio_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            collection = self.mongo_client[database_name][collectio_name]
            dataframe = pd.DataFrame(list(collection.find()))
            # drop the _id column 
            if "_id" in dataframe.columns.to_list():
                dataframe = dataframe.drop(columns=["_id"], axis="columns")
            # replace "na" with np.nan 
            dataframe.replace({"na": np.nan}, inplace=True)
            return dataframe
        
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def export_data_to_feature_store(self, dataframe: pd.DataFrame): 
        try: 
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # create folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e: 
            raise NetworkSecurityException(e, sys)


    def split_data(self, dataframe: pd.DataFrame): 
        try: 
            train_set, test_set = train_test_split(
                    dataframe, test_size = self.data_ingestion_config.test_test_spilt_ratio
                )
            logging.info("Data split spliting Completed")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting train and test file path")

            train_set.to_csv(
                    self.data_ingestion_config.training_file_path, index=False, header=True
                )
            test_set.to_csv(
                    self.data_ingestion_config.testing_file_path, index=False, header=True
                )
            
            logging.info("Exported train and test file path")

        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def IntiateDataIngestion(self):
        try: 
            dataframe = self.export_collection_as_datafram()
            dataframe = self.export_data_to_feature_store(dataframe)

        except Exception as e: 
            raise NetworkSecurityException(e, sys)