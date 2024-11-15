from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score, precision_score, recall_score
import os 
import sys
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME


class NetworkModel: 
    def __init__(self, preprocessor, model):
        try: 
            self.preprocessor = preprocessor
            self.model = model 
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
    def predict(self, X):
        X_transform = self.preprocessor.transform(X)
        yHat = self.model.predict(X_transform)
        return yHat
    
    