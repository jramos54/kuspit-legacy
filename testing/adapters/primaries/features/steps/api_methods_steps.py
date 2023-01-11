from behave import given, when, then, step
from parse import parse
import os, json
from dotenv import load_dotenv
from testing.common.logger_testing import Logger

load_dotenv()
logger=Logger("api_methods_step")
    
    
@when('Se envia una solicitud POST')
def step_request_post(context):
    try:
        payload=json.dumps(context.table_value,indent=4)
        access_token=context.accessToken
        context.requestApi.post_request(context.url,payload,access_token)
        logger.info(f"payload enviado {payload}")
    except:
        payload=json.dumps(context.table_value,indent=4)
        context.requestApi.post_request(context.url,payload)
        logger.info(f"payload enviado {payload}")
        
@when('Se envia una solicitud GET')
def step_request_get(context):
    params=context.params if hasattr(context, 'params') else None
    
    access_token=context.accessToken if hasattr(context, 'accessToken') else None
    
    if params:
        context.requestApi.get_request(context.url,access_token,**params)
        logger.info(f"Se envio una solicitud GET")
    else:
        context.requestApi.get_request(context.url,access_token)
        logger.info(f"Se envio una solicitud GET")


        
@when('Se envia una solicitud PATCH')
def step_request_patch(context):
    params=context.params if hasattr(context, 'params') else None
    access_token=context.accessToken if hasattr(context, 'accessToken') else None

    if params:
        context.requestApi.patch_request(context.url,access_token,**params)
        logger.info(f"Se envio una solicitud PATCH")
        
@when('Se envia una solicitud PUT')
def step_request_put(context):
    params=context.params if hasattr(context, 'params') else None
    payload=context.table_value
   
    if params:
        context.requestApi.put_request(context.url,context.accessToken,payload,**params)
        logger.info(f"Se envio una solicitud PUT")
    else:
        context.requestApi.put_request(context.url,context.accessToken,payload)
        logger.info(f"Se envio una solicitud PUT")