from networksecurity.components.Model import ModelTrainer
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_tranformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import ArtifactEntity, DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.logging.logging import logging
import os
import sys

if __name__ == "__main__":
    try:
        logging.info("Starting data ingestion process")
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation = DataValidation(data_validation_config=data_validation_config, artifact_entity=data_ingestion_artifact)
        data_validation_artifact = data_validation.initialize_data_validation_artifact()
        logging.info(f"Data validation artifact: {data_validation_artifact}")
        
        logging.info("Starting data transformation process")
        data_transformation_config = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"Data transformation artifact: {data_transformation_artifact}")
        
        logging.info("Starting model training process")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=model_trainer_config)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise NetworkSecurityException(e, sys)