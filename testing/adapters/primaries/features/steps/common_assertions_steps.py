from behave import given, when, then, step
from parse import parse
import os, json
from dotenv import load_dotenv
from testing.common.logger_testing import Logger


load_dotenv()
logger=Logger("common_assertions_steps")

@then('Se valida la respuesta codigo "{codigo}"') 
def step_response_code(context,codigo):
    response_code=context.requestApi.get_response_code()
    # logger.warning(context.requestApi.get_response())
    assert response_code==int(codigo), logger.assert_fail(f"El codigo obtenido es {response_code} y se esperaba {codigo}")
    logger.assert_pass(f"Se obtuvo un codigo de respuesta {response_code}") 
    
# @then('Se recibe un mensaje {mensaje}')
# def step_response_message(context,mensaje):
#     response=context.requestApi.get_response()
#     message=response.get('detail')
    
#     logger.info(context.text)
#     expected_message = context.text.strip() if context.text else mensaje.strip('"')
     
#     logger.warning(f"mensaje recibido {expected_message}")
#     logger.warning(f"mensaje esperado {expected_message}")
    
#     assert expected_message==message,logger.assert_fail(f"El mensaje recibido es diferente al esperado")
#     logger.assert_pass(f"El mensaje recibido coincide con el mensaje esperado")

@then('Se recibe un mensaje "{mensaje}"')
@then('Se recibe un mensaje')
def step_response_message(context, mensaje=None):
    response = context.requestApi.get_response()
    message = response.get('detail')

    # Usar el mensaje multilinea si está disponible, de lo contrario, usar el argumento
    if context.text:
        expected_message = context.text.strip()
    else:
        expected_message = mensaje.strip('"')

    # Normalizar saltos de línea
    message_normalized = "\n".join(line.strip() for line in message.splitlines()).strip()
    expected_message_normalized = "\n".join(line.strip() for line in expected_message.splitlines()).strip()

    logger.warning(f"Mensaje recibido: {message_normalized}")
    logger.warning(f"Mensaje esperado: {expected_message_normalized}")

    assert message_normalized == expected_message_normalized, logger.assert_fail(f"El mensaje recibido es diferente al esperado")
    logger.assert_pass(f"El mensaje recibido coincide con el mensaje esperado")
