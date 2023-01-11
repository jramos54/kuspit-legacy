import requests
from testing.common.logger_testing import Logger
from testing.engine.use_cases.secondaries.service_api_helper import APIHelper
from testing.adapters.primaries.features.steps.bank_steps import load_random_banks
from testing.common.config_urls import get_env_url,get_variable
from dotenv import load_dotenv
import os
from behave import model


load_dotenv()

logger=Logger("environment")

def before_feature(context, feature):
    load_random_banks(context, feature)
    


def before_scenario(context, scenario):
    context.requestApi = APIHelper()
    logger.warning("INICIO DE NUEVO ESCENARIO")
  
def after_scenario(context, scenario):
    logger.warning("FIN DEL ESCENARIO")
    
    if 'skip' in scenario.effective_tags:
        scenario.skip('marked with @skip')
    else:
        accessToken=context.accessToken
        refreshToken = context.refreshToken
        
        headers = {
            'Authorization': 'Bearer '+accessToken,
            'Content-Type': 'application/json'
        }

        variable=os.getenv("LOGOUT")
        url = get_env_url(variable)
        logger.info(url)
        data={
            "refresh":refreshToken
        }
        context.response = requests.post(url, headers=headers,json=data)
        logger.warning(context.response.json())
        
        if context.response.status_code == 200:
            logger.info('>>>\t\tLOGOUT EXITOSO\t\t<<<')
        else:
            logger.error('>>>\t\tLOGOUT FALLIDO\t\t<<<')
            
        if scenario.status == 'passed':
            mensaje = '===>\t\t\tEL ESCENARIO SE COMPLETO CON EXITO\t\t\t<==='
            logger.info(mensaje)
        else:# scenario.status=='failed':
            mensaje = '===>\t\tEL ESCENARIO NO SE PUDO COMPLETAR\t\t<==='
            logger.error(mensaje)
