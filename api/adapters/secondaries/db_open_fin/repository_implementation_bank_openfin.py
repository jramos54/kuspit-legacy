""" repository to connect to openfin"""
# librerias
# Variables de Configuración
# variables
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
# proyecto
from ....engine.domain.entities.entities_banks import Bank
from ....engine.use_cases.ports.secondaries import repository_bank as repository


class BankImplementation(repository.BankRepository):
    def get_bank(self, nombre: str, token: str) -> Bank:
        openfin_data = {"detail": "El proveedor no respondio exitosamente"}
        data = {"datos": {"filtro": nombre, "limite": 1}}
        authorization = {"Authorization": token}
        openfin_url = "http://" + OPENFIN_URL + "/rpc/instituciones_bancarias"

        try:
            openfin_response = requests.post(
                openfin_url, json=data, headers=authorization
            )
            print(f"openfin respondio {openfin_response.status_code}")

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()

                bank = Bank(
                    key=openfin_content["data"][0].get("key", 0),
                    nombre=openfin_content["data"][0].get("nombre", ""),
                    nombre_completo=openfin_content["data"][0].get(
                        "nombre_completo", ""
                    ),
                    rfc=openfin_content["data"][0].get("rfc", ""),
                )
                return bank
            else:
                print(openfin_response.json())
                response=openfin_response.json()
                return response

        except Exception as e:
            return openfin_data

    def list_banks(self, token: str) -> list:
        openfin_data = {"detail": "El proveedor no respondio exitosamente"}
        data = {"datos": {}}
        authorization = {"Authorization": token}
        openfin_url = "http://" + OPENFIN_URL + "/rpc/instituciones_bancarias"

        try:
            openfin_response = requests.post(
                openfin_url, json=data, headers=authorization
            )
            print(f"openfin respondio {openfin_response.status_code}")

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                list_bank = openfin_content["data"]

                return list_bank
            else:
                print(openfin_response.json())
                return openfin_data

        except Exception as e:
            return openfin_data
