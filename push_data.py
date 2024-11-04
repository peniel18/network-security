import os 
import sys 
import json
from dotenv import load_dotenv
import pandas as pd 
import numpy as np 
import pymongo 
from networksecurity.logging.logger import logging 
from networksecurity.exception.exception import NetworkSecurityException
import certifi


load_dotenv()
MANGO_DB_URI = os.getenv("MANGO_DB_URI")
ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        pass
        
    def csv_to_json(self, file_path):
        try: 
            data = pd.read_csv(file_path)
            data.head()
            data.reset_index(drop=True, inplace=True)
            # turn the dataframe into json
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try: 
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MANGO_DB_URI)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        
        except Exception as e: 
            NetworkSecurityException(e, sys)


if __name__ == "__main__":
    filepath = "Network_Data/phisingData.csv"
    database = "peniel18"
    collection = "NetworkData"
    dataExtractor = NetworkDataExtract()
    records = dataExtractor.csv_to_json(file_path=filepath)
    print(records)
    num_of_records = dataExtractor.insert_data_mongodb(records, database, collection)
    print(num_of_records)