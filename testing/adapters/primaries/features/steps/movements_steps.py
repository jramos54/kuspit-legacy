from behave import given, when, then, step
import os, json, random, copy
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from testing.engine.entities.entity_movement import Movements,HistoricalMovements
from pydantic import ValidationError
from testing.engine.entities.constants_bank import BANCOS
from behave import model
from datetime import datetime


load_dotenv()
logger=Logger("Movements_steps")

@then('Se valida el esquema de la respuesta de Movimientos')
def step_movements_validate_schema(context):
    response=context.requestApi.get_response()
    movements_data =response.get("data") if "data" in response.keys() else response
    # logger.warning(json.dumps(banks_data,indent=4))
    try:
        
        movimientos = Movements(movimientos=movements_data)
        logger.info("Los Movimientos tiene el esquema correcto.")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        assert False, f"Error de validación en: {e}"

@then('Se valida que no hay movimientos en la respuesta')
def step_validate_no_movements(context):
    response = context.requestApi.get_response()
    num_movimientos = len(response.get('data') or [])
    total_movements = (num_movimientos == 0)
        
    assert total_movements, logger.assert_fail(f"Se recibieron {num_movimientos} movimientos y deben ser cero")
    logger.assert_pass("No hay movimientos en el periodo")
    
@then('El numero de movimientos es menor al "{limite}"')
def step_validate_limit(context, limite):
    response = context.requestApi.get_response()
    num_movimientos = len(response.get('data') or [])

    try:
        limite = int(limite)
    except ValueError:
        raise ValueError(f"El valor del límite '{limite}' no es un número válido.")

    if limite == 0:
        limite = float('inf')
    
    assert num_movimientos <= limite, logger.assert_fail(f"El numero de movimientos es mayor al esperado: {num_movimientos} > {limite}")
    logger.assert_pass("El numero de movimientos corresponde al limite")
    
@then('Se validan el tipo de movimiento es "{movimiento}"')
def step_validate_movement_type(context, movimiento):
    response = context.requestApi.get_response()
    movimientos = response.get('data') or []

    for mov in movimientos:
        assert mov['movimiento'] == movimiento, logger.assert_fail(f"El movimiento '{mov['movimiento']}' no coincide con el esperado '{movimiento}'")
    
    logger.assert_pass(f"Todos los movimientos son del tipo '{movimiento}'")
    
@then('Se validan el estatus "{estatus}" del movimiento')
def step_validate_status_type(context, estatus):
    response = context.requestApi.get_response()
    movimientos = response.get('data') or []

    for mov in movimientos:
        assert mov['estatus'] == estatus, logger.assert_fail(f"El estatus '{mov['estatus']}' no coincide con el esperado '{estatus}'")
    
    logger.assert_pass(f"Todos los estatus son del tipo '{estatus}'")
    
@then('Valida el tipo de movimiento es "{movimiento}" y el estatus "{estatus}"')
def step_validate_status_movement_type(context, movimiento, estatus):
    response = context.requestApi.get_response()
    movimientos = response.get('data') or []

    for mov in movimientos:
        assert mov['movimiento'] == movimiento, logger.assert_fail(f"El movimiento '{mov['movimiento']}' no coincide con el esperado '{movimiento}'")
        assert mov['estatus'] == estatus, logger.assert_fail(f"El estatus '{mov['estatus']}' no coincide con el esperado '{estatus}'")
    
    logger.assert_pass(f"Todos los movimientos son del tipo '{movimiento}' y todos los estatus son del tipo '{estatus}'")


@then('Se valida el numero de elementos en la respuesta menor a 12')
def step_validate_months(context):
    response = context.requestApi.get_response()
    movimientos = response.get('data') or []

    assert len(movimientos) <= 12, logger.assert_fail(f"Hay mas meses de los permitidos")   
    logger.assert_pass(f"El historico de meses coincide con un año")

@then('Se valida el esquema de la respuesta de Movimientos Historico')
def step_historical_validate_schema(context):
    response=context.requestApi.get_response()
    movements_data =response.get("data") if "data" in response.keys() else response
    # logger.warning(json.dumps(banks_data,indent=4))
    try:
        
        historical = HistoricalMovements(movimientos=movements_data)
        logger.info("Los Movimientos tiene el esquema correcto.")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        assert False, f"Error de validación en: {e}"

@then('se valida el mes actual')
def step_current_months(context):
    response = context.requestApi.get_response()
    movimientos = response.get('data') or []

    # Obtener el mes actual en formato numérico
    current_month = datetime.now().month

    for movimiento in movimientos:
        if movimiento.get("mes") == current_month:
            assert movimiento.get("current"), logger.assert_fail(f"El mes actual no está seleccionado")
            logger.assert_pass(f"El mes actual está seleccionado")
            return
    logger.assert_fail(f"No se encontró un mes activo")