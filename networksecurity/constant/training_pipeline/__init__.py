import os 
import sys
import numpy as np
import pandas as pd

"""This module contains all the constant variables related to training pipeline"""

TARGET_COLUMN = "Result"
PIPELINE_NAME = "NetworkSecurityPipeline"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")
SAVED_MODEL_DIR = os.path.join(ARTIFACT_DIR, "saved_models")
MODEL_FILE_NAME = os.path.join(SAVED_MODEL_DIR, "model.pkl")


"""
Data Ingestion related constant start with DATA_INGESTION Var name"""

DATA_INGESTION_COLLECTION_NAME = "NetworkDataCollection"
DATA_INGESTION_DATABASE_NAME = "NetworkSecurityDB"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

"""Data Validation related constant start with DATA_VALIDATION Var name"""
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "valid"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_REPORT_FILE_NAME = "report.yaml"

"""Data Transformation related constant start with DATA_TRANSFORMATION Var name"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME: str = "transformed_object"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME: str = "transformed_train.npy"
DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME: str = "transformed_test.npy"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing_object.pkl"

## kkn imputer related nan value
DATA_TRANFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

"""Model Trainer related constant start with MODEL_TRAINER Var name"""
MODEL_TRAINER_DIR_NAME = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME = "model.pkl"
MODEL_EXPECTED_SCORE = 0.6
MODEL_TRAINED_OVER_FITTING_UNDER_FITTING_THRESHOLD = 0.05
