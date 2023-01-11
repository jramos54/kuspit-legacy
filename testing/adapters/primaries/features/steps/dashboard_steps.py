from behave import given, when, then, step
import os, json, random, copy
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from pydantic import ValidationError
from behave import model


load_dotenv()
logger=Logger("Dashboard_steps")

@then('Se valida el nombre "{full_name}" y asociado "{kasociado}"')
def step_response_validation(context, full_name,kasociado):
    response=context.requestApi.get_response()
    response_user =response.get("data") if "data" in response.keys() else response
    
    assert response_user.get("nombre")==full_name, logger.assert_fail(f"El nombre {response_user.get('nombre')} no coincide con {full_name}")
    logger.assert_pass(f"El nombre de usuario coincide")
    assert int(response_user.get("kasociado"))==int(kasociado), logger.assert_fail(f"El kasociado {response_user.get('kasociado')} no coincide con {kasociado}")
    logger.assert_pass(f"El kasociado de usuario coincide")


@then('El nombre completo es "{full_name}" y es nuevo usuario "{is_new_user}"')
def step_response_full_validation(context, full_name, is_new_user):
    response = context.requestApi.get_response()

    # Convertir is_new_user a booleano si es necesario
    is_new_user_bool = is_new_user.lower() == 'true' if isinstance(is_new_user, str) else is_new_user
    response_is_new_user = response.get("is_new_user")
    
    # Depuración: imprimir los valores y sus tipos
    print(f"Comparing: response_is_new_user ({response_is_new_user}) of type {type(response_is_new_user)} with is_new_user_bool ({is_new_user_bool}) of type {type(is_new_user_bool)}")

    assertion = False
    if response_is_new_user == is_new_user_bool:
        assertion = True
    
    assert response.get("full_name") == full_name, logger.assert_fail(f"El nombre {response.get('full_name')} no coincide con {full_name}")
    logger.assert_pass(f"El nombre de usuario coincide")
    assert assertion, logger.assert_fail(f"El estado {response_is_new_user} no coincide con {is_new_user_bool}")
    logger.assert_pass(f"El estado de usuario coincide")
