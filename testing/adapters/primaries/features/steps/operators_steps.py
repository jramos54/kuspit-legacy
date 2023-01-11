from behave import given, when, then, step
import os, json, random, copy
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from testing.engine.entities.entity_operators import Operators, Operator
from pydantic import ValidationError
from behave import model


load_dotenv()
logger=Logger("Operators_steps")

@then('Se valida el esquema de la respuesta de Operadores')
def step_operator_validate_schema(context):
    response=context.requestApi.get_response()
    operator_data =response.get("data") if "data" in response.keys() else response

    try:
        
        operators = Operators(operadores=operator_data)
        logger.info("Los Operadores tiene el esquema correcto.")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        assert False, f"Error de validación en: {e}"

@then('El campo acceso es "{acceso}"')
def step_operator_validate_acceso(context, acceso):
    response = context.requestApi.get_response()
    operator_data = response.get("data") if "data" in response.keys() else response

    # Crea una instancia de Operators con los datos de la respuesta
    operators = Operators(operadores=operator_data)

    # Accede al primer operador en la lista de operadores
    operator = operators.operadores[0]

    # Convierte el acceso esperado a booleano si es necesario
    if isinstance(acceso, str):
        acceso = acceso.lower() == 'true'

    # Valida que el campo acceso sea igual al valor esperado
    validation_acceso = operator.acceso == acceso

    # Realiza la aserción y registra el resultado
    assert validation_acceso, logger.assert_fail(f"El acceso es diferente al esperado. Esperado: {acceso}, Actual: {operator.acceso}")
    logger.assert_pass("El acceso es el esperado")


@then('El perfil del operador es "{perfil}"')
def step_operator_validate_perfil(context, perfil):
    response = context.requestApi.get_response()
    operator_data = response.get("data") if "data" in response.keys() else response

    # Crea una instancia de Operators con los datos de la respuesta
    operators = Operators(operadores=operator_data)

    # Accede al primer operador en la lista de operadores
    operator = operators.operadores[0]

    # Valida que el perfil del operador sea igual al valor esperado
    validation_perfil = operator.permisos.perfil

    # Realiza la aserción y registra el resultado
    assert validation_perfil == perfil, logger.assert_fail(f"El perfil es diferente al esperado. Esperado: {perfil}, Actual: {validation_perfil}")
    logger.assert_pass("El perfil es el esperado")
