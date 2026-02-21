import numpy as np
import pandas as pd
import sys
import os
from networksecurity.entity.config_entity import DataTransformationConfig, TrainingPipelineConfig, DataValidationConfig, DataIngestionConfig, ModelTrainerConfig
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging  import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object,load_object, load_numpy_array_data, evaluate_models
from networksecurity.entity.config_entity import DataTransformationConfig, TrainingPipelineConfig, DataValidationConfig, DataIngestionConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)
import mlflow
import dagshub
dagshub.init(repo_owner='AamirAhmed21', repo_name='Network-Security-System', mlflow=True)


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            logging.info(f"{'>>'*20}Model Trainer log started.{'<<'*20}")
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def tracking_mlflow(self, best_model_name, classification_score):
        try:
            with mlflow.start_run():
                f1_score = classification_score.f1_score
                precision_score = classification_score.precision_score
                recall_score = classification_score.recall_score
                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)
                mlflow.sklearn.log_model(best_model_name, "model")
                
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def train_model(self, x_train, y_train,x_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "AdaBoost": AdaBoostClassifier(),
                "Logistic Regression": LogisticRegression(),
                "Decision Tree": DecisionTreeClassifier(),}
            parmas = {
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "AdaBoost": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Logistic Regression": {
                    'C': [1, 5, 10, 15, 20, 25, 30]
                },
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss']
                }
            }
            model_report:dict = evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, param=parmas)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            logging.info(f"Best model is {best_model_name} with score {best_model_score}")
            y_train_pred = models[best_model_name].predict(x_train)
            
            classification_score = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            logging.info(f"Classification score for best model is: {classification_score}")
            
            ### TRACK THE MLFLOW USING MLFLOW
            self.tracking_mlflow(best_model_name=best_model_name, classification_score=classification_score)
            
            
            y_test_pred = models[best_model_name].predict(x_test)
            test_classification_score = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            logging.info(f"Classification score for best model on test data is: {test_classification_score}")
            
            self.tracking_mlflow(best_model_name=best_model_name, classification_score=test_classification_score)
            
            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
           
            Network_model = NetworkModel(model=models[best_model_name], preprocessor=preprocessor)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=Network_model)
            
            save_object('final_model/model.pkl', Network_model)
            ## Model Trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, train_metrics_artifact=classification_score, test_metrics_artifact=test_classification_score)
            logging.info(f"Model Trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info(f"Loading transformed training and testing data for model training.")
            x_train = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            x_test = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            
            x_train, y_train, x_test, y_test = x_train[:,:-1], x_train[:,-1], x_test[:,:-1], x_test[:,-1]
            
            model = self.train_model(x_train, y_train, x_test, y_test)
            return model
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e