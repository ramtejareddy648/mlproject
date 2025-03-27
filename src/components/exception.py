import sys
from src.components.logger import logging

def error_message_details(error_message, error_details: sys):
    _, _, er_tb = error_details.exc_info()
    filename = er_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        filename, er_tb.tb_lineno, str(error_message)
    )
    return error_message  # ✅ Fix: Return the formatted message

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        formated_message = error_message_details(error_message, error_details)
        super().__init__(formated_message)
        self.error_message = formated_message
    
    def __str__(self):
        return self.error_message
if __name__=='__main__':
    
    try:
        10/0
        
    except Exception as e:
        logging.info('zero division error')
        raise CustomException(str(e),sys)

    


