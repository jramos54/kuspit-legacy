""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto


class PasswordRecoveryImplementation:
    def __init__(self):
        self.url_token_temp = "http://" + OPENFIN_URL + "/rpc/token_temporal"
        self.url_questions = "http://" + OPENFIN_URL + "/rpc/preguntas"
        self.url_validate_questions = "http://" + OPENFIN_URL + "/rpc/preguntas_validar"
        self.url_change_password = "http://" + OPENFIN_URL + "/rpc/cambia_password"

    def create_token_temp(self,email:str,) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {
                "email": email
            }
        }
        headers = {'Content-Type': 'application/json'}

        try:
            openfin_response = requests.post(
                self.url_token_temp, json=data, headers=headers
            )

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()

                return openfin_content.get("data")

            else:

                return {"detail":"El correo no existe"}

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def get_questions(self,temp_token) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {}
        }
        headers = {
            'Authorization': 'Bearer '+temp_token,
            'Content-Profile': 'api_tmp',
            'Content-Type': 'application/json'
        }

        try:
            openfin_response = requests.post(
                self.url_questions, json=data, headers=headers
            )
            print(f"RESPUESTA OPEN FIN - {openfin_response.json()}")
            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()

                return openfin_content.get("data")

            else:

                return {"detail":"No se generaron preguntas"}

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def validate_questions(self,anwsers:list,temp_token:str) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        for answer in anwsers:
            if answer.get('id')==3:
                respuesta=answer.get('respuesta')
                respuesta=respuesta.replace('/','')
                answer['respuesta']=respuesta

        data = {
            "datos": {
                "preguntas": anwsers
            }
        }
        headers = {
            'Authorization': 'Bearer '+temp_token,
            'Content-Profile': 'api_tmp',
            'Content-Type': 'application/json'
        }
        print(data)
        try:
            openfin_response = requests.post(
                self.url_validate_questions, json=data, headers=headers
            )
            print(f"RESPUESTA OPEN FIN - {openfin_response.json()}")

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                data={
                    'code':int(openfin_content.get('code')),
                    'detail':openfin_content.get("data")
                }
                return data

            else:
                data = {
                    'code': 1,
                    "detail":"Respuestas no validas"
                }
                return data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def change_password(self,email:str,password:str,temp_token:str) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {
                "email": email,
                "password": password
            }
        }
        headers = {
            'Authorization':'Bearer ' +temp_token,
            'Content-Profile': 'api_tmp',
            'Content-Type': 'application/json'
        }

        try:
            openfin_response = requests.post(
                self.url_change_password, json=data, headers=headers
            )
            print(f"OPENFIN - {openfin_response.json()}\nOPENFIN CODE {openfin_response.status_code}")
            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                if openfin_content.get("code") == '0':
                    return {"detail":"La contraseña se cambio exitosamente",
                            'code':200}
                else:
                    return {"detail": "El tiempo expiro"}

            else:

                return {"detail":"No se pudo cambiar el password"}

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data
