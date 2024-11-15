from networksecurity.components.data_ingestion import DataIngestion 
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.components.model_trainer import ModelTrainer
import os
import sys



if __name__ == "__main__":
    trainingPipeline = TrainingPipelineConfig()
    dataIngestionConfig = DataIngestionConfig(trainingPipeline)
    data_ingestion = DataIngestion(data_ingestion_config=dataIngestionConfig)
    

    # validation 
    dataIngestionArtifact = data_ingestion.IntiateDataIngestion()
    print(dataIngestionArtifact)
    data_validation_config = DataValidationConfig(trainingPipeline)
    dataVal = DataValidation(data_ingestion_artifact=dataIngestionArtifact ,data_validation_config=data_validation_config)
    dataValArtifact = dataVal.initiate_data_validation()
    print(dataValArtifact)

    dataTransConfig = DataTransformationConfig(trainingPipeline)
    dataTrans = DataTransformation(
                    data_validation_artifact = dataValArtifact, 
                    data_transformation_config = dataTransConfig
                )
    dataTransArtifact = dataTrans.InitiateDataTransformation()
    print(dataTransArtifact)

    modelTrainerConfig = ModelTrainerConfig(trainingPipeline)
    modelTrainer = ModelTrainer(
        model_trainer_config=modelTrainerConfig, 
        data_transformation_artifact=dataTransArtifact
    )
    modeltrainerArtifact = modelTrainer.InitialModelTrainer()
    print(modeltrainerArtifact)