import os 
import sys
import json 

from dotenv import load_dotenv
import certifi

import pandas as pd
import numpy as np
import pymongo

from networksecurity.logging.logging import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

MONDB_URL = os.getenv('MONDB_URL')
print(f"MONDB_URL: {MONDB_URL}")


ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONDB_URL, tlsCAFile=ca)
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise NetworkSecurityException(e, sys)
    def cv_to_json_convertor(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            json_data = list(json.loads(df.T.to_json()).values())
            return json_data
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {e}")
            raise NetworkSecurityException(e, sys)
    def insert_data_to_mongodb(self, data, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.data = data
            
            self.mongo_client = pymongo.MongoClient(MONDB_URL)
            
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.data)
            logging.info("Data inserted successfully into MongoDB")
            return (len(self.data))
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {e}")
            raise NetworkSecurityException(e, sys)
if __name__ == "__main__":
    FILE_PATH = os.path.join(os.getcwd(), 'Network_Data', "phisingData.csv")
    
    DATABASE = "NetworkSecurityDB"
    COLLECTION = "NetworkDataCollection"
    networkobj = NetworkDataExtract()
    json_data = networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    
    print(f"JSON data: {json_data}")

    no_of_records = networkobj.insert_data_to_mongodb(data=json_data, database=DATABASE, collection=COLLECTION)
    print(f"Number of records inserted: {no_of_records}")



