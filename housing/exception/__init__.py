import sys
import os
import sys


class HousingException(Exception):
    
    def __init__(self, error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.error_message = HousingException.get_detailed_error_message(error_message,sys)

    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_details:sys) -> str:

        """
            error_message: Exception Object
            error_detail: Object of sys module 
        """

        _,_,exec_tb = error_details.exc_info()
        lineno = exec_tb.tb_frame.f_lineno
        filename = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error Occured in [{filename}] at line no : [{lineno}] and error_message is : [{error_message}]"
        return error_message

    def __str__(self):
        return self.error_message


    def __repr__(self):
        return HousingException.__name__.str()

    
