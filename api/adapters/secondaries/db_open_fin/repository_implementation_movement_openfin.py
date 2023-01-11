""" repository to conect to openfin"""
import json
# Librerias Estandar
import typing
from datetime import datetime

# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
from ....engine.domain.entities.entities_movement import Movement
from ....engine.use_cases.ports.secondaries import repository_movement as repository

from ....adapters.secondaries.factory import (
    constructor_recipient as recipient_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_recipient as recipient_engine,
)
recipients_repository = recipient_repository.constructor_recipient()
recipients_engine = recipient_engine(recipients_repository)

class MovementsImplementation(repository.MovementRepository):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/cuenta_movimientos"

    def list_movements_by_account(self, *args, **kwargs) -> typing.List[Movement]:
        print("consulta con open fin ")
        token = args[0] if args else None

        kauxiliar = kwargs.get("kauxiliar", None)
        limite = kwargs.get("limite", None)
        authorization = {"Authorization": token}

        defecha = kwargs.get("defecha", None)
        afecha = kwargs.get("afecha", None)

        if defecha:
            defecha_str = defecha.strftime(
                "%Y-%m-%d"
            )  # Convierte date a string en el formato correcto
            defecha = datetime.strptime(defecha_str, "%Y-%m-%d").strftime("%d/%m/%Y")

        if afecha:
            afecha_str = afecha.strftime(
                "%Y-%m-%d"
            )  # Convierte date a string en el formato correcto
            afecha = datetime.strptime(afecha_str, "%Y-%m-%d").strftime("%d/%m/%Y")

        data = {
            "datos": {
                "kauxiliar": kauxiliar,
                "defecha": defecha,
                "afecha": afecha,
                "limite": limite,
            }
        }

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            # print(f"openfin respondio {openfin_response.status_code}")
            # print(f"OPEN_FIN: response movements {json.dumps(openfin_response.json(),indent=4)}")

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()

                if openfin_content["data"] is None:
                    return []
                else:
                    list_movements = openfin_content["data"]["movimientos"]
                    movements=self.movements_transformation(list_movements,token)
                    return movements
            else:
                response_openfin = {
                    "status_code": openfin_response.status_code,
                    "detail": openfin_response.json(),
                }
                return response_openfin

        except Exception as error_exception:
            return {"openfin_data": "Error en la conexion con openfin"}

    def movements_transformation(self, list_movements, token):
        destinatarios_openfin = recipients_engine.list_recipient(token=token)

        for movement in list_movements:
            id_destinatario = movement.get('iddestinatario')
            id_cuenta = movement.get('idcuenta')

            # Multiplica el monto por -1 si el movimiento no es "Depósito"
            if movement.get("movimiento") != "Depósito":
                movement['monto'] *= -1

            # Filtra el destinatario en función de id_destinatario
            destinatario_openfin = next(
                (destinatario for destinatario in destinatarios_openfin if
                 destinatario.get('iddestinatario') == id_destinatario),
                None
            )

            if destinatario_openfin:
                # Actualiza pfisica en el movimiento
                movement['pfisica'] = destinatario_openfin.get('pfisica')

                # Busca la cuenta que coincida con id_cuenta
                cuenta_encontrada = None
                for cuenta in destinatario_openfin.get('cuentas', []):
                    if id_cuenta == cuenta.get('idcuenta'):
                        movement['institucion_bancaria'] = cuenta.get('institucion_bancaria')
                        cuenta_encontrada = cuenta
                        break

                if cuenta_encontrada is None:
                    print(f"No matching cuenta found for idcuenta {id_cuenta} in destinatario {id_destinatario}")

        return list_movements


