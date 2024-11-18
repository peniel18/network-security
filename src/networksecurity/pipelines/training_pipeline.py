from networksecurity.components.data_ingestion import DataIngestion 
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.components.model_trainer import ModelTrainer
import os
import sys



class TrainingPipeline: 
    def __init__(self): 
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            dataIngestionArtifact = data_ingestion.IntiateDataIngestion()
            logging.info(f"Data Ingestion completed")
            return dataIngestionArtifact

        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info("Data Validation has Started")
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            dataValidation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            dataValidationArtifact = dataValidation.initiate_data_validation()
            logging.info("Data Validation has been completed")
            return dataValidationArtifact
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try: 
            logging.info("Data Transformation has Started")
            data_transforamtion_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            Data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transforamtion_config)
            DataTransArtifact = Data_transformation.InitiateDataTransformation()
            return DataTransArtifact
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try: 
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            modelTrainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            modelTrainerArtifact = modelTrainer.InitialModelTrainer()
            return modelTrainerArtifact
        except Exception as e: 
            raise NetworkSecurityException(e, sys)