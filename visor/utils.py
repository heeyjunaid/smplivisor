import os
import logging

def init_logger(name: str):
    # Use the same settings as above for root logger
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))    

    # Create a console handler and set its logging level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
