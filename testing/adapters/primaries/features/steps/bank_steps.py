from behave import given, when, then, step
import os, json, random, copy
from dotenv import load_dotenv
from testing.common.logger_testing import Logger
from testing.engine.entities.entity_bank import Bank,Banks
from pydantic import ValidationError
from testing.engine.entities.constants_bank import BANCOS
from behave import model


load_dotenv()
logger=Logger("Bank_steps")

@then('Se valida el esquema de la respuesta de Bancos')
def step_bank_validate_schema(context):
    response=context.requestApi.get_response()
    banks_data =response.get("data") if "data" in response.keys() else response
    # logger.warning(json.dumps(banks_data,indent=4))
    try:
        if isinstance(banks_data,list):
            banks = Banks(bancos=banks_data)
        else:
            bank=Bank(**banks_data)
        logger.info("La respuesta tiene el esquema correcto.")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        assert False, f"Error de validación en: {e}"
        
@then('Se valida la informacion del banco "{nombre}", clave "{key}", rfc "{rfc}" y nombre completo "{nombre_completo}"')
def step_bank_validate_data(context, nombre, key, rfc, nombre_completo):
    response = context.requestApi.get_response()
    
    # Asumimos que 'response' es un diccionario
    logger.info(f"Response: {json.dumps(response, indent=4)}")
    banco = response.get("data") if "data" in response.keys() else response

    rfc_=banco.get('rfc', ' ') if banco.get('rfc', ' ') != "" else " "
    nombre_completo_=banco.get('nombre_completo', ' ') if banco.get('nombre_completo', '') != "" else " "

    # Validar la información del banco directamente del diccionario
    assert banco.get("key") == int(key), logger.assert_fail(f"Expected key {key}, but got {banco.get('key')}")
    assert banco.get("nombre") == nombre, logger.assert_fail(f"Expected nombre {nombre}, but got {banco.get('nombre')}")
    assert rfc_ == rfc.strip('"'), logger.assert_fail(f"Expected rfc {rfc}, but got {rfc_}")
    assert nombre_completo_ == nombre_completo.strip('"'), logger.assert_fail(f"Expected nombre_completo {nombre_completo}, but got {nombre_completo_}")

def load_random_banks(context, feature):
    dynamic_scenarios = (s for s in feature.scenarios if isinstance(s, model.ScenarioOutline) and 'dynamic_banks' in s.tags)
    for scenario in dynamic_scenarios:
        for example in scenario.examples:
            orig = copy.deepcopy(example.table.rows[0])
            example.table.rows = []
            selected_banks = random.sample(BANCOS, 25)
            for bank in selected_banks:
                row = copy.deepcopy(orig)
                row.cells = [bank['nombre'], str(bank['key']), bank.get('rfc'," "), bank.get('nombre_completo'," ")]
                example.table.rows.append(row)
    
