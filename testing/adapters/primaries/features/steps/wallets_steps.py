from behave import given, when, then, step
import os, json, random, copy
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from testing.engine.entities.entity_wallet import Products,Wallets
from pydantic import ValidationError
from behave import model
from datetime import datetime


load_dotenv()
logger=Logger("Wallets_steps")

@then('Se valida el esquema para productos')
def step_product_validate_schema(context):
    response=context.requestApi.get_response()
    products_data =response.get("data") if "data" in response.keys() else response
    # logger.warning(json.dumps(banks_data,indent=4))
    
    try:
        if isinstance(products_data,list): 
            products = Products(productos=products_data)
            logger.assert_pass("Los productos tienen el esquema correcto.")
        elif isinstance(products_data,dict):
            products = Products(productos=[products_data])
            logger.assert_pass("Los productos tienen el esquema correcto.")
    except ValidationError as e:
        assert False, logger.assert_pass(f"Error de validación en: {e}")
        

@then('Se valida el esquema para wallets')
def step_wallet_validate_schema(context):
    response=context.requestApi.get_response()
    wallets_data =response.get("data") if "data" in response.keys() else response
    # logger.warning(json.dumps(banks_data,indent=4))
    try:
        if isinstance(wallets_data,list):
            wallets = Wallets(wallets=wallets_data)
            logger.assert_pass("Las wallet tienen el esquema correcto.")
        elif isinstance(wallets_data,dict):
            wallets = Wallets(wallets=[wallets_data])
            logger.assert_pass("Las wallet tienen el esquema correcto.")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        assert False, f"Error de validación en: {e}"

