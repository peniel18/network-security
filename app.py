from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import training_pipeline, DataIngestionConfig, TrainingPipelineConfig




trainingPipelineConfig = TrainingPipelineConfig()
dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
dataIngestion = DataIngestion(dataIngestionConfig)
dataIngestion.IntiateDataIngestion()