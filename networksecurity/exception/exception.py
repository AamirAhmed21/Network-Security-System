import sys


from networksecurity.logging.logging import logging

class NetworkSecurityException(Exception):
    def __init__(self, error_message, errors_details:sys):
        self.error_message = error_message
        _, _, exc_tb = errors_details.exc_info()
        
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename
    def __str__(self):
        return "Error occurred in script: [{0}] at line number: [{1}] with error message: [{2}]".format(
            self.filename, self.lineno, str(self.error_message))
# if __name__ == "__main__":
#     try:
#         logging.info("Testing the NetworkSecurityException")
#         a = 1/0
#     except Exception as e:
#         logging.info("Divide by zero error")
#         raise NetworkSecurityException(e, sys)
