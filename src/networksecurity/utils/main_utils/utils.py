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
        with open(file_path, "rb") as yaml_file: 
            return yaml.safe_load(yaml_file)
    except Exception as e: 
        logging.error("Error Ocurred in function read_yaml_file in utils")
        raise NetworkSecurityException(e, sys)
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None: 
    try: 
        if replace: 
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file: 
            yaml.dump(content, file)

    except Exception as e: 
        NetworkSecurityException(e, sys)