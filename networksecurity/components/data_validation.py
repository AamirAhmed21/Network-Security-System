
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yamal_file, write_yaml_file
from scipy.stats import ks_2samp
import os
import sys
import pandas as pd
import numpy as np

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20}Data Validation log started.{'<<'*20}")
            self.data_validation_config = data_validation_config
            self.artifact_entity = data_ingestion_artifact
            self.schema_file_path = read_yamal_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_num_columns = len(self.schema_file_path['columns'])
            actual_num_columns = len(dataframe.columns)
            logging.info(f"Expected number of columns: {expected_num_columns}")
            logging.info(f"Actual number of columns: {dataframe.shape[1]}")
            actual_num_columns = dataframe.shape[1]
            if expected_num_columns == actual_num_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold = 0.05) -> bool:
        report = {}
        try:
            drift_detected = False
            for column in base_df.columns:
                if column in current_df.columns:
                    stat, p_value = ks_2samp(base_df[column], current_df[column])
                    if p_value < threshold:  # If p-value is less than threshold, we consider it as drift
                        logging.info(f"Data drift detected in column: {column}")
                        drift_detected = True
                        report.update({column: {"p_value": p_value, "drift_detected": True}})
                    else:
                        logging.info(f"No data drift detected in column: {column}")
                        report.update({column: {"p_value": p_value, "drift_detected": False}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
                ## creating the directory
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return drift_detected, report
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initialize_data_validation_artifact(self) -> DataValidationArtifact:
        try:
            train_file_path = self.artifact_entity.trained_file_path
            test_file_path = self.artifact_entity.test_file_path
            
            ## read the data from train and test data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            
            ## validate the data and get the valid and invalid data file path
            status = self.validate_number_of_columns(train_df)
            if not status:
                error_message = f"Train data does not have the expected number of columns. Expected: {len(self.schema_file_path['columns'])}, Actual: {train_df.shape[1]}"
                logging.error(error_message)
            status = self.validate_number_of_columns(test_df)
            if not status:
                error_message = f"Test data does not have the expected number of columns. Expected: {len(self.schema_file_path['columns'])}, Actual: {test_df.shape[1]}"
                logging.error(error_message)
            
            ## Check if the data has the numerical columns exist or not
            numerical_columns = self.schema_file_path['numerical_columns']
            for column in numerical_columns:
                if column not in train_df.columns:
                    error_message = f"Train data does not have the expected numerical column: {column}"
                    logging.error(error_message)
                if column not in test_df.columns:
                    error_message = f"Test data does not have the expected numerical column: {column}"
                    logging.error(error_message)
            ## lets check datadrift
            status = self.detect_data_drift(train_df, test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_data_dir)
            os.makedirs(dir_path, exist_ok=True)
            
            train_df.to_csv(self.data_validation_config.valid_data_dir, index=False)
            test_df.to_csv(self.data_validation_config.invalid_data_dir, index=False)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_trained_file_path=self.data_validation_config.valid_data_dir,
                valid_test_file_path=self.data_validation_config.invalid_data_dir,
                invalid_trained_file_path=self.data_validation_config.invalid_data_dir,
                invalid_test_file_path=self.data_validation_config.invalid_data_dir,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
             
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            return self.initialize_data_validation_artifact()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

