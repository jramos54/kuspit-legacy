""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto


class EmailNotificationImplementation:
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/enviar_email"

    def send_email(self,email:str,titulo:str,mensaje:str,token: str) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {
                "email": f"{email}",
                "titulo": f"{titulo}",
                "mensaje": f"{mensaje}"
            }
        }
        authorization = {"Authorization": token}

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()

                return openfin_content.get("message")

            else:

                return "No se pudo enviar el correo"

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data
