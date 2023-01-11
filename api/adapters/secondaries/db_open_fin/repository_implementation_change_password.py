from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto


class ChangePasswordImplementation:
    def __init__(self):
        self.url_change_password = "http://" + OPENFIN_URL + "/rpc/apife1"

    def change_password(self,old_password:str,new_password:str,password_confirmation:str,token:str) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
          "recurso": "usuario/cambiaClave",
          "params": {
            "anterior": old_password,
            "nueva": new_password,
            "confirma": password_confirmation
          }
        }
        headers = {
            'Authorization':token,
            'Content-Type': 'application/json'
        }

        try:
            openfin_response = requests.post(
                self.url_change_password, json=data, headers=headers
            )
            print(f"OPENFIN - response {openfin_response}")
            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                if openfin_content.get("ok"):
                    return {"detail":"La contraseña se cambio exitosamente",
                            'code':200}
                else:
                    return {"detail": "No se pudo cambiar el password"}

            else:

                return {"detail":"No se pudo cambiar el password"}

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data
