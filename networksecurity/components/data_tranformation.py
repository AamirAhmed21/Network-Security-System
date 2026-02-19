import sys 
import os
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import  DATA_TRANFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logging  import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            logging.info(f"{'>>'*20}Data Transformation log started.{'<<'*20}")
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def get_data_transformer_object(self) -> Pipeline:
        try:
            knn_imputer = KNNImputer(**DATA_TRANFORMATION_IMPUTER_PARAMS)
            return Pipeline(steps=[
                ("knn_imputer", knn_imputer)
            ])
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Reading valid train and test file for data transformation.")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_trained_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info(f"Splitting input and target feature from both train and test dataframe.")
            x_train = train_df.drop(TARGET_COLUMN, axis=1)
            y_train = train_df[TARGET_COLUMN]

            x_test = test_df.drop(TARGET_COLUMN, axis=1)
            y_test = test_df[TARGET_COLUMN]
            
            y_train = y_train.replace(-1,0)
            y_test = y_test.replace(-1,0)

            logging.info(f"Applying KNN Imputer on training and testing data.")
            preprocessor = self.get_data_transformer_object()
            x_train_arr = preprocessor.fit_transform(x_train)
            x_test_arr = preprocessor.transform(x_test)

            logging.info(f"Concatenating input and target features for train and test data.")
            train_arr = np.c_[x_train_arr, y_train]
            test_arr = np.c_[x_test_arr, y_test]
            
            ## save the transformed training and testing arrays and preprocessor object

            logging.info(f"Saving transformed training and testing arrays.")
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor)
            
            logging.info(f"Creating data transformation artifact.")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e