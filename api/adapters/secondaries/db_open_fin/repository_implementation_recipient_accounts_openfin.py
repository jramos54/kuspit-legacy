""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
from ....engine.domain.entities.entities_recipient_accounts import RecipientAccount
from ....engine.use_cases.ports.secondaries import (
    repository_recipient_accounts as repository,
)


class RecipientAccountImplementation(repository.RecipientAccountRepository):
    def __init__(self):
        self.url_cuenta_destinatario = (
            "http://" + OPENFIN_URL + "/rpc/destinatario_cuenta"
        )

    def create_recipient_account(
        self,
        iddestinatario: int,
        cuenta: int,
        institucion_bancaria: str,
        catalogo_cuenta: str,
        is_active: bool,
        limite_operaciones: int,
        limite: float,
        alias: str,
        token: str,
    ) -> RecipientAccount:
        """
        Crea un destinatario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {
                "iddestinatario": iddestinatario,
                "cuenta": cuenta,
                "institucion_bancaria": institucion_bancaria,
                "catalogo_cuenta": catalogo_cuenta,
                "is_active": is_active,
                "limite_operaciones": limite_operaciones,
                "limite": limite,
                "alias": alias,
            }
        }
        authorization = {"Authorization": token}
        try:
            response_openfin = requests.post(
                self.url_cuenta_destinatario, json=data, headers=authorization
            )
            print(f"status de cuenta destinatario {response_openfin.status_code}")
            cuenta_destinatario = response_openfin.json()

            idcuenta = cuenta_destinatario["data"]["idcuenta"]

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return response_openfin.json()

        try:
            open_fin_url = "http://" + OPENFIN_URL + "/rpc/destinatarios"
            openfin_info = {"datos": {"iddestinatario": iddestinatario}}
            authorization = {"Authorization": token}
            response_openfin = requests.post(
                open_fin_url, json=openfin_info, headers=authorization
            )
            print(f"status de destinatario {response_openfin.status_code}")
            print(response_openfin.json())
            if response_openfin.status_code == 200:
                openfin_data_res = response_openfin.json()

                cuentas_destinatario = openfin_data_res["data"][0]["cuentas"]
                cuenta_creada = None
                for cuenta_ in cuentas_destinatario:
                    if cuenta_["idcuenta"] == idcuenta:
                        cuenta_creada = cuenta_
                        break

                recipient_account = RecipientAccount(
                    idcuenta=cuenta_creada["idcuenta"],
                    cuenta=cuenta_creada["cuenta"],
                    institucion_bancaria=cuenta_creada["institucion_bancaria"],
                    catalogo_cuenta=cuenta_creada["catalogo_cuenta"],
                    is_active=cuenta_creada["activo"],
                    limite_operaciones=cuenta_creada["limite_operaciones"],
                    limite=cuenta_creada["limite"],
                    alias=cuenta_creada["alias"],
                )
                return recipient_account

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

        return openfin_data

    def update_recipient_account(
        self,
        idcuenta: int,
        is_active: bool,
        limite_operaciones: int,
        limite: float,
        alias: str,
        token: str,
    ) -> RecipientAccount:
        """
        Actualiza un destinatario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {
                "idcuenta": idcuenta,
                "is_active": is_active,
                "limite_operaciones": limite_operaciones,
                "limite": limite,
                "alias": alias,
            }
        }
        authorization = {"Authorization": token}
        try:
            response_openfin = requests.post(
                self.url_cuenta_destinatario, json=data, headers=authorization
            )

            response_openfin.json()
            print(f"status de cuenta destinatario {response_openfin.status_code}")
        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

        try:
            open_fin_url = "http://" + OPENFIN_URL + "/rpc/destinatarios"
            openfin_info = {"datos": {}}
            authorization = {"Authorization": token}
            response_openfin = requests.post(
                open_fin_url, json=openfin_info, headers=authorization
            )
            print(f"status de destinatario {response_openfin.status_code}")
            print(response_openfin.json())  # List of dicts
            if response_openfin.status_code == 200:
                openfin_data_res = response_openfin.json()

                response_destinatarios = openfin_data_res["data"]  # ["destinatarios"]

                cuenta_creada = None
                for destinatario in response_destinatarios:
                    cuentas_destinatarios = destinatario["cuentas"]
                    for cuenta in cuentas_destinatarios:
                        if cuenta["idcuenta"] == idcuenta:
                            cuenta_creada = cuenta
                            break
                if cuenta_creada is not None:
                    recipient_account = RecipientAccount(
                        idcuenta=cuenta_creada["idcuenta"],
                        cuenta=cuenta_creada["cuenta"],
                        institucion_bancaria=cuenta_creada["institucion_bancaria"],
                        catalogo_cuenta=cuenta_creada["catalogo_cuenta"],
                        is_active=cuenta_creada["activo"],
                        limite_operaciones=cuenta_creada["limite_operaciones"],
                        limite=cuenta_creada["limite"],
                        alias=cuenta_creada["alias"],
                    )
                    print(recipient_account)
                    return recipient_account

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

        return openfin_data

    def delete_recipient_account(
        self, idcuenta: int, iddestinatario: int, token: str
    ) -> any:
        """
        Actualiza un destinatario con la info dada
        """
        print(f"{type(idcuenta)}, {type(iddestinatario)}")
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        open_fin_url = "http://" + OPENFIN_URL + "/rpc/destinatario_cuenta_elimina"
        data = {"datos": {"idcuenta": idcuenta, "iddestinatario": iddestinatario}}
        authorization = {"Authorization": token}
        print(data)
        try:
            response_openfin = requests.post(
                open_fin_url, json=data, headers=authorization
            )
            print(f"status de cuenta destinatario {response_openfin.status_code}")
            print(f"contenido de respuesta de openfin {response_openfin.json()}")

            return response_openfin.status_code

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data
