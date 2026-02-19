from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
import os
import sys

from networksecurity.utils.main_utils.utils import load_object, save_object


class NetworkModel:
    def __init__(self, model, preprocessor):
        self.model = model
        self.preprocessor = preprocessor

    def predict(self, X):
        try:
            logging.info(f"Using preprocessor to transform the input data.")
            transformed_X = self.preprocessor.transform(X)
            logging.info(f"Making predictions using the trained model.")
            predictions = self.model.predict(transformed_X)
            return predictions
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
