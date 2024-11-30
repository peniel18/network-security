from networksecurity.components.data_ingestion import DataIngestion 
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.cloud.s3_syncer import S3Sync 
import os
import sys



class TrainingPipeline: 
    def __init__(self): 
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

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
    
    def sync_artifact_dir_to_s3(self):
        """
        Push artifacts to s3 with timestamps 
        """
        try: 
            s3_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(
                folder = self.training_pipeline_config.artifact_dir, 
                aws_bucket_url = s3_bucket_url 
            )
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
    # push model artifacts to s3 bucket
    def sync_model_to_dir_s3(self):
        """
        Push model artifacts to s3 with timestamps
        """
        try:
            s3_model_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(
                folder = self.training_pipeline_config.model_dir, 
                aws_bucket_url = s3_model_url
            )
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def runPipeline(self):
        try:
            dataIngestionArtifact = self.start_data_ingestion()
            dataValidationArtifact = self.start_data_validation(data_ingestion_artifact=dataIngestionArtifact)
            dataTransformationArtifact = self.start_data_transformation(data_validation_artifact=dataValidationArtifact)
            modelTrainerArtifact = self.start_model_trainer(data_transformation_artifact=dataTransformationArtifact)
            self.sync_artifact_dir_to_s3()
            self.sync_model_to_dir_s3()
            return modelTrainerArtifact
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.runPipeline()
    