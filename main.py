from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
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
    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise NetworkSecurityException(e, sys)