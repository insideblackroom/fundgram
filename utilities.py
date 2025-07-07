import logging.config
import json

def load_logging_config(logging_config_path):
    with open(logging_config_path, 'r') as f:
        logging_config = json.load(f)
    logging.config.dictConfig(logging_config)


