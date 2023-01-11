""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
from ....engine.domain.entities.entities_user_dashboard import UserDashboard
from ....engine.use_cases.ports.secondaries import repository_user_dashboard as repository


class UserDashboardImplementation(repository.UserDashboardRepository):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/apife1"

    def get_user_dashboard(self,token: str) -> UserDashboard:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "recurso": "usuario/info",
            "params": {}
        }
        authorization = {"Authorization": token}

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                user_dashboard = UserDashboard(
                    nombre=openfin_content["data"]["nombre"],
                    correo=openfin_content["data"]["email"],
                    kasociado=openfin_content["data"]["__kasociado"]
                )
                return user_dashboard

            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data
