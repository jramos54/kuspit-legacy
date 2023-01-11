""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
from ....engine.domain.entities.entities_recipient import Recipient
from ....engine.use_cases.ports.secondaries import repository_recipient as repository


class RecipientImplementation(repository.RecipientRepository):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/destinatarios"

    def get_recipient(self, iddestinatario: int, token: str) -> Recipient:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        data = {"datos": {"iddestinatario": iddestinatario}}
        authorization = {"Authorization": token}
        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                recipient = Recipient(
                    iddestinatario=openfin_content["data"][0]["iddestinatario"],
                    nombre=openfin_content["data"][0]["nombre"],
                    paterno=openfin_content["data"][0]["paterno"],
                    materno=openfin_content["data"][0]["materno"],
                    # alias=openfin_content["data"]["destinatarios"][0]["alias"],
                    rfc=openfin_content["data"][0]["rfc"],
                    curp=openfin_content["data"][0]["curp"],
                    is_active=openfin_content["data"][0]["is_active"],
                    correo=openfin_content["data"][0]["correo"],
                    pfisica=openfin_content["data"][0]["pfisica"],
                    cuentas=openfin_content["data"][0]["cuentas"],
                )
                return recipient

            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def list_recipient(self, token: str) -> list:
        """list the recipients"""
        openfin_data = {"detail": "El proveedor no respondio exitosamente"}
        data = {"datos": {}}
        authorization = {"Authorization": token}

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            print(f"openfin respondio {openfin_response.status_code}")

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                list_recipients = openfin_content["data"]  # ["destinatarios"]

                return list_recipients
            else:
                print(openfin_response.json())
                return openfin_data

        except Exception as error_exception:
            return openfin_data

    def create_recipient(
        self,
        nombre: str,
        paterno: str,
        materno: str,
        rfc: str,
        curp: str,
        is_active: bool,
        correo: str,
        pfisica: bool,
        token: str,
    ) -> Recipient:
        """
        Crea un destinatario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        try:
            open_fin_url = "http://" + OPENFIN_URL + "/rpc/destinatario"
            if pfisica:
                # Si es persona física y RFC o CURP están vacíos
                if rfc == "" or curp == "":
                    openfin_info = {
                        "datos": {
                            "nombre": nombre,
                            "paterno": paterno,
                            "materno": materno,
                            "pfisica": pfisica,
                            "correo": correo,
                            "is_active": is_active,
                        }
                    }
                else:
                    openfin_info = {
                        "datos": {
                            "nombre": nombre,
                            "paterno": paterno,
                            "materno": materno,
                            "pfisica": pfisica,
                            "correo": correo,
                            "rfc": rfc,
                            "curp": curp,
                            "is_active": is_active,
                        }
                    }
            else:
                # Si es persona moral y RFC está vacío
                if rfc == "":
                    raise ValueError(
                        f"RFC es requerido")
                openfin_info = {
                    "datos": {
                        "nombre": nombre,
                        "paterno": paterno,
                        "materno": materno,
                        "pfisica": pfisica,
                        "correo": correo,
                        "rfc": rfc,
                        "is_active": is_active,
                    }
                }

            authorization = {"Authorization": token}
            response_openfin = requests.post(
                open_fin_url, json=openfin_info, headers=authorization
            )
            print(f"status de creacion de destinatario {response_openfin.status_code}")
            print(response_openfin.json())
            if response_openfin.status_code == 201:
                openfin_data_res = response_openfin.json()

                iddestinatario = openfin_data_res["data"]["iddestinatario"]
                print(iddestinatario)
                recipient = self.get_recipient(iddestinatario, token)

                return recipient
            else:
                return response_openfin.json()["message"]

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

    def update_recipient(
        self,
        iddestinatario: int,
        nombre: str,
        paterno: str,
        materno: str,
        rfc: str,
        curp: str,
        is_active: bool,
        correo: str,
        pfisica: bool,
        token: str,
    ) -> Recipient:
        """
        Actualiza un destinatario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        try:
            open_fin_url = "http://" + OPENFIN_URL + "/rpc/destinatario"

            if pfisica:
                openfin_info = {
                    "datos": {
                        "iddestinatario": iddestinatario,
                        "nombre": nombre,
                        "paterno": paterno,
                        "materno": materno,
                        "pfisica": pfisica,
                        "correo": correo,
                        "rfc": rfc,
                        "curp": curp,
                        "is_active": is_active,
                    }
                }
            else:
                openfin_info = {
                    "datos": {
                        "iddestinatario": iddestinatario,
                        "nombre": nombre,
                        "paterno": paterno,
                        "materno": materno,
                        "pfisica": pfisica,
                        "correo": correo,
                        "rfc": rfc,
                        "is_active": is_active,
                    }
                }

            authorization = {"Authorization": token}
            response_openfin = requests.post(
                open_fin_url, json=openfin_info, headers=authorization
            )
            print(f"status de update destinatario {response_openfin.status_code}")
            print(response_openfin.json())
            if response_openfin.status_code == 200:
                openfin_data_res = response_openfin.json()

                iddestinatario = openfin_data_res["data"]["iddestinatario"]
                recipient = self.get_recipient(iddestinatario, token)

                return recipient

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

    def delete_recipient(self, iddestinatario: int, token: str) -> any:
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            open_fin_url = "http://" + OPENFIN_URL + "/rpc/destinatario_elimina"
            openfin_info = {"datos": {"iddestinatario": iddestinatario}}
            authorization = {"Authorization": token}
            response_openfin = requests.post(
                open_fin_url, json=openfin_info, headers=authorization
            )
            print(f"status de destinatario {response_openfin.status_code}")
            print(response_openfin.json())
            if response_openfin.status_code == 200:
                openfin_data_res = response_openfin.json()
                data_response = {"code": 200, "data": openfin_data_res}
                return data_response
            elif response_openfin.status_code == 400:
                openfin_data_res = response_openfin.json()
                data_response = {"code": 400, "data": openfin_data_res}
                return data_response
            else:
                openfin_data_res = response_openfin.json()
                data_response = {"code": 404, "data": openfin_data_res}
                return data_response

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

        return openfin_data
