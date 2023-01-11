from behave import given, when, then, step
from parse import parse
import os, json, time
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from testing.common.config_urls import get_variable,get_env_url


load_dotenv()
logger=Logger("common_steps")


@given('El url "{url}"')
def step_given_url(context,url):
    variable=get_variable(url)
    context.url=get_env_url(variable)   
    logger.info(f"Consumir el endpoint {context.url}")
    
    
@step('Se obtienen los valores de la tabla')
def step_get_table(context):
    if len(context.table.rows) == 1:
        row = context.table.rows[0]
        user_dict = {heading: get_variable(row[heading]) for heading in context.table.headings}
        context.table_value=user_dict
        logger.info(f"Se obtuvo el siguiente dato {json.dumps(context.table_value)}")
    else:
        # Si hay más de una fila, crea una lista de diccionarios
        user_dicts = []
        for row in context.table:
            user_dict = {heading: get_variable(row[heading]) for heading in context.table.headings}
            user_dicts.append(user_dict)
        
        context.table_values= user_dicts
        logger.info(f"Se obtuvo una lista con {len(context.table_values)} elementos")


@then('Se obtienen los valores del texto')
def step_get_text(context):
    context.payload_json = json.loads(context.text)
    
@step('los tokens de la sesion de usuario')
def step_get_tokens(context):
    response=context.requestApi.get_response()
    context.accessToken=response.get('access')
    context.refreshToken=response.get('refresh')
    logger.info(f"AccesToken:\n{context.accessToken}")
    logger.info(f"RefreshToken:\n{context.refreshToken}")
    
@step('Se hace una espera de "{espera}" segundos')
def step_espera(context,espera):
    logger.warning(f"inicia una espera de {int(espera)} segundos")
    time.sleep(int(espera))
    logger.info("la espera ha terminado, el flujo continua")
    
@step('Los params enviados en la solicitud')
def step_get_params(context):
    context.params = {row['key']: row['Value'] for row in context.table}
    logger.warning(context.params)
      
