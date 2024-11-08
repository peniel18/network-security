import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np 
import dill
import pickle 



def read_yaml_file(file_path: str) -> dict: 
    logging.info("function: read_yaml_file has started")
    try: 
        with open(file=file_path, "rb") as yaml_file: 
            return yaml.safe_load(yaml_file)
    except Exception as e: 
        logging.error("Error Ocurred in function read_yaml_file in utils")
        raise NetworkSecurityException(e, sys)