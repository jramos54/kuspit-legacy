"""Respository implementacion open fin with account engine"""
# Librerias Estandar
import typing

# Variables de Configuración
# settings
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
from ....engine.domain.entities.entities_accounts import AccountsOpenFin, Accounts

# engine
from ....engine.use_cases.ports.secondaries import repository_account as repository


class AccountImpl(repository.Account):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/cuentas"
        self.url_creacion = "http://" + OPENFIN_URL + "/rpc/cuenta_nueva"

    def get_account(self, kauxiliar: int, token: str) -> AccountsOpenFin:
        """get account with the type_account and name in openfin are kauxiliar y alias"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            data = {"datos": {"kauxiliar": kauxiliar}}
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            if openfin_response.status_code == 200:
                accounts_data = openfin_response.json()
                account = AccountsOpenFin(
                    alias=accounts_data["data"]["cuentas"][0]["alias"],
                    clabe=accounts_data["data"]["cuentas"][0]["clabe"],
                    activo=accounts_data["data"]["cuentas"][0]["activo"],
                    saldo=accounts_data["data"]["cuentas"][0]["saldo"],
                    kauxiliar=accounts_data["data"]["cuentas"][0]["kauxiliar"],
                )

                return account
            else:
                print(f"account response: {openfin_response.json()}")
                openfin_data = openfin_response.json()
                return openfin_data
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al crear Cuenta nueva")
            return openfin_data

    def create_account(
        self,
        alias: str,
        type_account: int,
        token: str,
    ) -> Accounts:
        """
        Create new account
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            openfin_info = {
                "datos": {
                    "idproducto": type_account,
                    "aka": alias,
                }
            }
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_creacion, json=openfin_info, headers=authorization
            )
            print(f"status de wallet {openfin_response.status_code}")
            print(openfin_response.json())
            if openfin_response.status_code == 201:
                openfin_data = openfin_response.json()
                kauxiliar = openfin_data["data"]["idtransaccion"]
                openfin_data = self.get_account(kauxiliar, token)
                # Creamos entidad Account
                account = Accounts(
                    alias=openfin_data["alias"],
                    type_account=openfin_data["idproducto"],
                )

                return account
            else:
                return openfin_response.json()["message"]
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al crear destinatario")
            return openfin_data

    def list_accounts(self, token: str) -> typing.Union[list, dict]:
        """
        list all account by kauxiliar
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            data = {"datos": {}}
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            if openfin_response.status_code == 200:
                accounts_data = openfin_response.json()

                accounts_list = accounts_data["data"]["cuentas"]

                return accounts_list
            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al crear Cuenta nueva")
            return openfin_data
