from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.logging.logging import logging

## configuration for data ingestion component

from networksecurity.entity.config_entity import DataIngestionConfig

from networksecurity.entity.artifact_entity import ArtifactEntity

import os 
import sys
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import pymongo
from typing import List

from dotenv import load_dotenv
load_dotenv()

MONDB_URL = os.getenv('MONDB_URL')

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info(f"DataIngestionConfig: {self.data_ingestion_config}")
        except Exception as e:
            logging.error(f"Error initializing DataIngestion: {e}")
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        '''
        Docstring for export_collection_as_dataframe
        
        :param self: Description
        :return: Description
        :rtype: DataFrame
        and to read the data from MongoDB collection and convert it into a DataFrame
        '''
        try:
            logging.info("Exporting MongoDB collection to DataFrame")
            
            # Create MongoDB client
            client = pymongo.MongoClient(MONDB_URL)
            logging.info("Successfully connected to MongoDB")
            
            # Access the database and collection
            db = client[self.data_ingestion_config.database_name]
            collection = db[self.data_ingestion_config.collection_name]
            
            # Fetch data from MongoDB
            data = list(collection.find())
            logging.info(f"Fetched {len(data)} records from MongoDB")
            
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            logging.info("Data converted to DataFrame successfully")
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
            
            df.replace({'na': np.nan}, inplace=True)
            
            return df
        
        except Exception as e:
            logging.error(f"Error exporting collection as DataFrame: {e}")
            raise NetworkSecurityException(e, sys)
    
    def export_data_as_feature_store(self, dataframe: pd.DataFrame) -> str:
        try:
            logging.info("Exporting data to feature store")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            dataframe.to_csv(self.data_ingestion_config.feature_store_file_path, index=False)
            logging.info(f"Data exported to feature store at {self.data_ingestion_config.feature_store_file_path}")
            return self.data_ingestion_config.feature_store_file_path
        except Exception as e:
            logging.error(f"Error exporting data to feature store: {e}")
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test sets")
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            logging.info(f"Data split into train and test sets with ratio {self.data_ingestion_config.train_test_split_ratio}")
            
            # Save train and test sets to respective file paths
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_file_path), exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False)
            
            logging.info(f"Train set saved at {self.data_ingestion_config.training_file_path}")
            logging.info(f"Test set saved at {self.data_ingestion_config.test_file_path}")
        except Exception as e:
            logging.error(f"Error splitting data into train and test sets: {e}")
            raise NetworkSecurityException(e, sys)
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            
            self.export_data_as_feature_store(dataframe=dataframe)
            
            self.split_data_as_train_test(dataframe=dataframe)
            
            DataIngestionArtifact = ArtifactEntity(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return DataIngestionArtifact
            
        except Exception as e:
            logging.error(f"Error during data ingestion: {e}")
            raise NetworkSecurityException(e, sys)

