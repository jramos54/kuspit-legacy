from dotenv import load_dotenv
import os
from testing.common.logger_testing import Logger

logger=Logger("url config")

load_dotenv()

def get_url(variable):
    environment = os.getenv('ENVIRONMENT')
    
    if environment == "LOCAL":
        BASE_URL = os.getenv('LOCAL')
    elif environment == "SERVER":
        BASE_URL = os.getenv('SERVER')
    else:
        raise ValueError("ENVIRONMENT debe ser 'LOCAL' o 'SERVER'")

    return f"{BASE_URL}{variable}"

def get_variable(text):
    if text.startswith('$'):
        variable=os.getenv(text[1:])
        return variable
    else:
        return text

def get_env_url(text):
    url=get_url(text)
    return url
