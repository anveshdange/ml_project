'''
This code traines our Machine Learning Model  \

'''
# IMPORTS 
import os 
import sys 

from dataclasses import dataclass 
from catboost import CatBoostRegressor 
from sklearn.ensemble import (
    AdaBoostRegressor ,
    GradientBoostingRegressor ,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score 
from sklearn.neighbors import KNeighborsRegressor 
from sklearn.tree import DecisionTreeRegressor 
from xgboost import XGBRegressor

from src.exception import CustomException 
from src.logger import logging 
from src.utils import save_object
from src.utils import evaluate_model


@dataclass
class ModelTrainerConfig: 
    trained_model_file_path : str = os.path.join('artifacts' , 'model.pkl')

class ModelTrainer :
    def __init__(self):
        self.model_trainer_config : ModelTrainerConfig = ModelTrainerConfig() 
    
    def initiate_model_training(self, train_array, test_array) :
        try: 
            logging.info("Splitting Training and Testing Input Data" )
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1] ,
                test_array[:, :-1],
                test_array[:, -1]
            )
            models = {
                "Random Forest": RandomForestRegressor() ,
                "Decision Tree": DecisionTreeRegressor() ,
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression() ,
                "K-Neighbors Classifier" : KNeighborsRegressor() ,
                "XGB Classifier" : XGBRegressor() ,
                "CatBoosting Classifer": CatBoostRegressor(verbose=False) ,
                "AdaBoost Classifier": AdaBoostRegressor()
            }

            model_report : dict = evaluate_model(
                X_train=X_train, 
                y_train=y_train,
                X_test=X_test, 
                y_test=y_test,
                models=models
            )

            # get best model score from the dictionary 
            best_model_score = max(sorted(model_report.values()))
            # get best model name from the dictionary 
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            if best_model_score<0.6 :
                raise CustomException("No Best Model Found", sys)
            logging.info("Best model found on both Training and Testing set") 

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path ,
                obj = best_model 
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted) 

            return r2_square 

        except Exception as e:
            raise CustomException(e, sys)
