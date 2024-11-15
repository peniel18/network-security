import os 
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from networksecurity.utils.main_utils.utils import save_object, load_numpy_array_data, load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

class ModelTrainer: 
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact): 
        try: 
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact 
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
    def train_model(self, X_train, y_train):
        models = {
            "Random Forest" : RandomForestClassifier(verbose=1), 
            "Decision Tree" : DecisionTreeClassifier(), 
            "Gradient Boosting" : GradientBoostingClassifier(verbose=1),
            "Logistic Regression" : LogisticRegression(verbose=1),
            "ADABoost": AdaBoostClassifier(), 
        }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },

            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },

            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },

            "Logistic Regression":{},
            
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
        
    def InitialModelTrainer(self) -> ModelTrainerArtifact: 
        try: 
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            testing_file_path = self.data_transformation_artifact.transformed_test_file_path
            # load numpy arrays 
            trainArr = load_numpy_array_data(train_file_path)
            testArr = load_numpy_array_data(testing_file_path)
            # spliting the data
            x_train, y_train, x_test, y_test = (
                trainArr[:, :-1],
                trainArr[:, -1],
                testArr[:, :-1],
                testArr[:, -1],
            )

            model = self.train_model(x_train, y_train)


            
        except Exception as e: 
            raise NetworkSecurityException(e, sys)