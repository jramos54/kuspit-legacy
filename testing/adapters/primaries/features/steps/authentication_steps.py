from behave import given, when, then, step
import os, json
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from testing.engine.assertions.assert_authentication import TokenAssertion
from testing.adapters.primaries.features.steps.api_methods_steps import step_request_post
from testing.adapters.primaries.features.steps.common_assertions_steps import step_response_code,step_response_message
from testing.adapters.primaries.features.steps.common_steps import step_espera


load_dotenv()
logger=Logger("authentication_steps")

@then('Se recibe un access token y un refresh token')
def step_token_validation(context):
    token_assertions = TokenAssertion(context.accessToken, context.refreshToken, logger)
    
    assert token_assertions.assertion_access_result
    assert token_assertions.assertion_refresh_result

@when('Se realizan los siguientes intentos')
def step_intentos_login(context):
    for row in context.table:
        intento = row['intento']
        codigo = row['codigo']
        mensaje = row['mensaje']
        espera = row['espera']
        
        logger.info(f"se inicia un login con las credenciales {context.table_value}")
        step_request_post(context)
        logger.info(f"Respuesta de la api {context.requestApi.get_response()}")
        step_response_code(context,codigo)
        step_response_message(context,mensaje)
        step_espera(context,espera)
        
        logger.info(f"El intento {intento} se ha completado")