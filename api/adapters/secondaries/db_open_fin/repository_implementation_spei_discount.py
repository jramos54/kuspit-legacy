from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto


class SpeiDiscountImplementation:
    def __init__(self):
        self.url_openfin = "http://" + OPENFIN_URL + "/rpc/apife1"

    def spei_discount(self,kauxiliar:int,idcuentab:int,token:str) -> dict:
        """get a recipient by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
          "recurso": "wallets/asignaDescuento",
          "params": {
            "kauxiliar": kauxiliar,
            "idcuentab": idcuentab
          }
        }
        headers = {
            'Authorization':token,
            'Content-Type': 'application/json'
        }

        try:
            openfin_response = requests.post(
                self.url_openfin, json=data, headers=headers
            )
            print(f"OPENFIN - response {openfin_response}")
            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                if openfin_content.get("ok"):
                    return {"detail":f"Descuento de primer spei asignado a la cuenta destino {idcuentab}",
                            'code':200}
                else:
                    return {"detail": "No se pudo asignar la cuenta para descuento"}

            else:

                return {"detail":"No se pudo asignar la cuenta para descuento"}

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data
