"""Respository implementacion open fin with payments engine"""
# Librerias Estandar
import typing
from datetime import timedelta, datetime

# Variables de Configuración
# settings
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

from api.engine.use_cases.factory import orm_mapper

# Librerías de Terceros
import requests

# Proyecto
from ....engine.domain.entities.entities_payments import PaymentsOpenFin

# engine
from ....engine.use_cases.ports.secondaries import repository_payments as repository


class PaymentsImpl(repository.Payments):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/pagos"
        self.url_creacion = "http://" + OPENFIN_URL + "/rpc/pago"
        self.url_borrar = "http://" + OPENFIN_URL + "/rpc/cuenta_pago_borrar"

    def get_payments(
        self, id_transaction, date, to_date, token: str
    ) -> PaymentsOpenFin:
        """list payments with range of dates in openfin"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            data = {"datos": {"defecha": date, "afecha": to_date}}
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            if openfin_response.status_code == 200:
                payments_data = openfin_response.json()

                payments_list = payments_data["data"]["pagos"]
                try:
                    payment_info = [
                        d for d in payments_list if d.get("__rowId") == id_transaction
                    ]
                    return payment_info[0]
                except KeyError:
                    print(
                        "No se encontro el pago con el id_transaccion {}.".format(
                            id_transaction
                        )
                    )
                    return openfin_data

            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al consultar un pago")
            return openfin_data

    def create_payment(
        self,
        kauxiliar: int,
        id_recipient: int,
        id_account: int,
        amount: float,
        description: str,
        payment_date: str,
        reference: str,
        payment_hour: str,
        token: str,
    ) -> PaymentsOpenFin:
        """
        Create new account
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
      
        try:
            if payment_hour == None:
                formatted_payment_date_str = payment_date.strftime("%d/%m/%Y")
                openfin_info = {
                    "datos": {
                        "kauxiliar": kauxiliar,
                        "iddestinatario": id_recipient,
                        "idcuenta": id_account,
                        "monto": amount,
                        "descripcion": description,
                        "fechapago": formatted_payment_date_str,
                        "referencia": reference,
                    }
                }
                
            else:
                formatted_payment_date_str = payment_date.strftime("%d/%m/%Y")
                formatted_payment_hour_str = payment_hour.strftime("%H:%M:%S")

                openfin_info = {
                    "datos": {
                        "kauxiliar": kauxiliar,
                        "iddestinatario": id_recipient,
                        "idcuenta": id_account,
                        "monto": amount,
                        "descripcion": description,
                        "fechapago": formatted_payment_date_str,
                        "referencia": reference,
                        "Hora de pago": formatted_payment_hour_str,
                    }
                }

            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_creacion, json=openfin_info, headers=authorization
            )
           
            # TODO: solicitar a openfin cambio de status code en reponse
            if openfin_response.status_code == 200:
                openfin_data = openfin_response.json()
                id_transaction = openfin_data["data"]["idtransaccion"]
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
                payment = self.get_payments(
                    id_transaction, yesterday, formatted_payment_date_str, token
                )
                return orm_mapper.constructor_payment_openfin_entities(payment)
            else:
                return openfin_response.json()["message"]
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al consultar pago")
            return openfin_data

    def list_payments(self, date, to_date, token: str) -> typing.List[PaymentsOpenFin]:
        """list payments with range of dates in openfin"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            formatted_date_str = date.strftime("%d/%m/%Y")
            formatted_to_date_str = to_date.strftime("%d/%m/%Y")
            data = {
                "datos": {
                    "defecha": formatted_date_str,
                    "afecha": formatted_to_date_str,
                }
            }
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            if openfin_response.status_code == 200:
                payments_data = openfin_response.json()

                payments_list = payments_data["data"]["pagos"]

                return [
                    orm_mapper.constructor_payment_openfin_entities(payment)
                    for payment in payments_list
                ]
            elif openfin_response.status_code == 400:
                openfin_data_res = openfin_response.json()
                openfin_data = {"code": 400, "data": openfin_data_res}
                return openfin_data
            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al consultar los pagos")
            return openfin_data

    def delete_payment(self, id_transaction: int, token: str) -> any:
        """Delete payments with id transaction"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            data = {"datos": {"idtransaccion": id_transaction}}
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_borrar, json=data, headers=authorization
            )
            if openfin_response.status_code == 200:
                openfin_data_res = openfin_response.json()
                openfin_data = {"code": 200, "data": openfin_data_res}

            elif openfin_response.status_code == 400:
                openfin_data_res = openfin_response.json()
                openfin_data = {"code": 400, "data": openfin_data_res}

            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al eliminar el pago")
            return openfin_data
        return openfin_data
