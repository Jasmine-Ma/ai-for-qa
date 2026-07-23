import os
import inspect
import logging


def custom_logger(log_level=logging.DEBUG):
    # Gets the name of the class / method from where this method is called
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    # By default, log all messages
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("automation.log", mode='a')
    file_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def check_file_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path))


def create_file(path):
    with open(path, "a") as my_file:
        my_file.write("")

