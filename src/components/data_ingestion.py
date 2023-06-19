# importing 
import os 
import sys 

# modular imports 
from src.exception import CustomException 
from src.logger import logging 
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig 
from src.components.model_trainer import ModelTrainerConfig 
from src.components.model_trainer import ModelTrainer 

import pandas as pd 
from sklearn.model_selection import train_test_split 
from dataclasses import dataclass # python 3.9 onwards 

# Data Ingestion Configurations
@dataclass
class DataIngestionConfig:
    '''
    This class holds the paths for files/folders during the Data Ingestion Phase 
    '''
    train_data_path : str = os.path.join('artifacts', 'train.csv')
    test_data_path : str = os.path.join('artifacts', 'test.csv') 
    raw_data_path : str = os.path.join('artifacts', 'data.csv') 

# Data Ingestion Class 
class DataIngestion :
    '''
    This is a Data Ingestion Class
    '''
    # Class Constructor 
    def __init__(self) :
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self) :

        '''
        Function creates train.csv, test.csv and data.csv in folders \ 
        specified in the DataIngestionConfig class.
        '''

        logging.info("Entered the Data Ingestion Method or components") 
        try :
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Exported/Read the Dataset as a Pandas DataFrame. Sucess!")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info('Train Test Split Initiated')

            train_set, test_set = train_test_split(df,test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) 
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) 
            logging.info("Ingestion of the Data is Completed")

            return (
                self.ingestion_config.train_data_path , 
                self.ingestion_config.test_data_path
            )

        except Exception as exc:
            raise CustomException(exc, sys)

if __name__ == "__main__" :
    obj = DataIngestion() 
    data_transformation = DataTransformation()
    train_data, test_data = obj.initiate_data_ingestion()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_path= obj.ingestion_config.train_data_path, 
        test_path= obj.ingestion_config.test_data_path
    )

    model_trainer = ModelTrainer()
    p = model_trainer.initiate_model_training(
        train_array = train_arr, 
        test_array = test_arr, 
    )
    print(p)