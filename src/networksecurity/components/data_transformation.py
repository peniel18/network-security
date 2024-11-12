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
            logging.info(f"Reading data at file Path {file_path}")
            return pd.read_csv(file_path)
        except Exception as e: 
            raise NetworkSecurityException(e, sys) 

    def get_data_transformer_object(cls) -> Pipeline: 
        """
        Construct a data transformation pipeline with a KNN imputer
        
        Returns:
            sklearn.pipeline.Pipeline: A data transformation pipelin
        
        """
        logging.info("get_data_transformation_object has started")
        try: 
            knnImputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline(
                [
                    ("Imputer", knnImputer)
                ]
            )
            return processor 
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
            
            processor = self.get_data_transformer_object()
            preprocessor = processor.fit(train_features)
            transformed_train_features = preprocessor.transform(train_features)
            transformed_test_features = preprocessor.transform(test_features)

            train_data = np.c_[transformed_train_features, np.array(train_target)]
            test_data = np.c_[transformed_test_features, np.array(test_target)]

            save_numpy_array_data(
                    self.data_transformation_config.transformed_train_file_path, array=train_data
                )
            save_numpy_array_data(
                    self.data_transformation_config.transformed_test_file_path, array=test_data
                )
            save_object(self.data_transformation_config.transformed_object_file_path, obj=preprocessor)

            data_transformation_artifact = DataTransformationArtifact(
                                                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path, 
                                                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path, 
                                                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path 
                                            )

            return data_transformation_artifact

        except Exception as e: 
            raise NetworkSecurityException(e, sys)