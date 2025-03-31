import os
import sys
import pandas as pd 
import numpy as np
from src.components.logger import logging
from src.components.exception import CustomException
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.utlis import save_object


@dataclass
class DatatransferConfig:
    process_obj_path=os.path.join('data_files','processor.pkl')




class DataTransfer:
    
    def __init__(self):
        self.data_transfer_config=DatatransferConfig()
    
    
    def data_transfer_obj(self):
        
        
        logging.info('inside data_transfer_obj')
        
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            
            numerical_pipe=Pipeline(
                steps=[
                    ('simpleimputer',SimpleImputer(strategy='median')),
                    ('standardscale',StandardScaler())
                ]
            )
            logging.info('numerical pipeline is created')
            
            categorical_pipe=Pipeline(steps=[
                
                ('simpleimputer',SimpleImputer(strategy="most_frequent")),
                ('onehotencodeing',OneHotEncoder(sparse_output=False)),
                ('standarscale',StandardScaler())
                
            ])
            logging.info('categorical pipeline is created')
            
            
            
            processor=ColumnTransformer(
                transformers=[
                    ('numeric',numerical_pipe,numerical_columns),
                    ('categotical',categorical_pipe,categorical_columns)
                ]
            
                
            )
            
            logging.info('processor object is created')
            
            return processor
            
            
        except Exception as e:
            raise CustomException(str(e),sys)
    
    
    def data_transfer_initation(self,train_path,test_path):
        try:
            
            train_df=pd.read_csv(train_path)
            logging.info('train df is read inside data_transfer_initation ')
            test_df=pd.read_csv(test_path)
            logging.info('test df is read inside data_transfer_initation ')
            
            target_column='math_score'
            x_train=train_df.drop(columns=[target_column],axis=1)
            y_train=train_df[target_column]
            logging.info('x_train and y_train data is divided')
            x_test=test_df.drop(columns=[target_column],axis=1)
            y_test=test_df[target_column]
            logging.info('x_test and y_test is loaded')
            
            preprocess_obj=self.data_transfer_obj()
            
            logging.info('preprocessor object is loaded')
            x_train_processed=preprocess_obj.fit_transform(x_train)
            x_test_processed=preprocess_obj.transform(x_test)
            
            logging.info('x_train and x_test is processed')
            
            train_arr=np.c_[x_train_processed,np.array(y_train)]
            test_arr=np.c_[x_test_processed,np.array(y_test)]
            
            logging.info('train and test array is done')
            
            save_object(
                obj_path=self.data_transfer_config.process_obj_path,
                obj=preprocess_obj
            )
            
            
            return(
                train_arr,
                test_arr
            )
            
        except Exception as e:
            raise CustomException(str(e),sys)
        