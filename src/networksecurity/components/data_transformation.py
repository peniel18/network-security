import sys
import os 
import pandas as pd 
import numpy as np 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline 
from networksecurity.constant.training_pipeline import TARGET_COLUMN 
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging 
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self,
     data_validation_artifact: DataValidationArtifact,
     data_transformation_config: DataTransformationConfig
     ):
        try: 
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame: 
        try: 
            return pd.read_csv(file_path)
        except Exception as e: 
            raise NetworkSecurityException(e, sys) 


    def InitiateDataTransformation(self) -> DataTransformationArtifact:
        logging.info("Data Transformation has Started")
        try: 
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            # drop target column 
            train_features = train_df.drop(columns=[TARGET_COLUMN], axis="columns")
            train_target_feature = train_df[TARGET_COLUMN]
            train_target = train_target_feature.replace(-1, 0)
            
            test_features = test_df.drop(columns=[TARGET_COLUMN], axis="columns")
            test_target_feature = test_df[TARGET_COLUMN]
            test_target = test_target_feature.replace(-1, 0)

            
        except Exception as e: 
            raise NetworkSecurityException(e, sys)