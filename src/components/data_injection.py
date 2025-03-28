import os
import sys
from src.components.exception import CustomException
from src.components.logger import logging
from dataclasses import dataclass
import pandas as pd 
from sklearn.model_selection import train_test_split


@dataclass
class Dataingestionconfig:
    train_path :str=os.path.join('data_files','train.csv')
    test_path :str=os.path.join('data_files','test.csv')
    data_path :str=os.path.join('data_file','data.csv')



class DataingestionInitiation:
    def __init__(self):
        self.data_ingestion_config=Dataingestionconfig()
    
    def data__ingestion_initiation(self):
        logging.info('data ingestion is started')
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('stud file is load into dataset as df variable')
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.data_path),exist_ok=True)
            df.to_csv(self.data_ingestion_config.data_path,index=False,header=True)
            train_set,test_set=train_test_split(df,test_size=0.20,random_state=45)
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_path),exist_ok=True)
            test_set.to_csv(self.data_ingestion_config.test_path,index=False,header=True)
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_path),exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.train_path,header=True,index=False)
            
            
            logging.info('ingestion is completed')
            
            return(
                self.data_ingestion_config.train_path,
                self.data_ingestion_config.test_path
            )
            
            
            
            
            
        except Exception as e:
            raise CustomException(str(e),sys)
    




if __name__=="__main__":
    
    
    obj=DataingestionInitiation()
    train_data,test_data=obj.data__ingestion_initiation()
