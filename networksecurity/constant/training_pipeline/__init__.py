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

"""
Data Ingestion related constant start with DATA_INGESTION Var name"""

DATA_INGESTION_COLLECTION_NAME = "NetworkDataCollection"
DATA_INGESTION_DATABASE_NAME = "NetworkSecurityDB"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2