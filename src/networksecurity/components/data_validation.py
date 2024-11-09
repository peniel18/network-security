from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file
from scipy.stats import ks_2samp
from typing import Set 
import pandas as pd 
import os 
import sys



class DataValidation: 
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try: 
            logging.info("Data Validation has Started")
            self.data_ingestion_artifact = data_ingestion_artifact 
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e: 
            logging.error("Error Ocurred in data_validation.py")
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame: 
        try: 
            return pd.read_csv(file_path)
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool: 
        try: 
            #logging.info("validate_number_of_columns as started ")
            num_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {num_of_columns}")
            logging.info(f"DataFrame columns: {len(dataframe.columns)}") 
            # check 
            if len(dataframe.columns) == num_of_columns: 
                return True
            else: 
                return False 
        except Exception as e: 
            logging.error("Erorr occured in validate_number_of_columns as started ")
            raise NetworkSecurityException(e, sys)

    def validateNumericalColumns(self, dataframe: pd.DataFrame) -> bool: 
        """
        Validate if dataframe columns dtypes matches the Expected dtypes

        Args:   
            dataframe (pd.DataFrame): DataFrame to validate 
        
        Returns:
            bool: True if all columns mactch expected, otherwise False
        
        """
        try: 
            scheme_file = self._schema_config
            numerical_cols = scheme_file["numerical_columns"]
            # create set that stores strings 
            ExpectedDataTypes = {str(dtype) for column in scheme_file["columns"] 
                                for dtype in column.values()    }

            # validate each columns data type 
            for col in dataframe[numerical_cols].columns: 
                if  str(dataframe[col].dtype) not in ExpectedDataTypes: 
                    return False 
            return True 
        
        except Exception as e: 
            logging.error(f"Error validaing numerical columns: {str(e)}")
            NetworkSecurityException(e, sys)

        
        #print(numericalColumns)

    def initiate_data_validation(self) ->  DataIngestionArtifact: 
        try: 
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            # read teh data from train and test 
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            # validata number of columns 
            TrainStatus = self.validate_number_of_columns(dataframe=train_dataframe)
            TestStatus = self.validate_number_of_columns(dataframe=test_dataframe)
            if not TrainStatus: 
                error_message = f"Train DataFrame does not contain the required number of columns"
                logging.info(error_message)

            if not TestStatus: 
                error_message = f"Test DataFrame does not contain the required number of columns"
                logging.info(error_message)


        except Exception as e: 
            logging.error("Error occured in intiate_data_validation")
            raise NetworkSecurityException(e, sys)
        

    
if __name__ == "__main__":
    dataV = DataValidation(DataIngestionArtifact)
    dataV.validateNumericalColumns()