from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file
from scipy.stats import k2_2samp
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