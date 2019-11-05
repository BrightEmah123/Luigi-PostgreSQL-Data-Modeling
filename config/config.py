import os
from configparser import ConfigParser

config = ConfigParser()
CONFIG_DIR = os.path.abspath(os.path.join('__FILE__', '../config/config.cfg'))
config.read(os.path.join(CONFIG_DIR))

def conn_config():
    database = {}
    if config.has_section('POSTGRESQL'):
        params = config.items('POSTGRESQL')
        for param in params:
            database[param[0]] = param[1]
    return database