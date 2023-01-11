""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto

class RecipientBatchImplementation:
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/apife1"

    def import_recipients(self, filename: str,recipients:list, token: str):
        """import a recipients"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data ={
            "recurso": "proveedores/impBeneficiarios",
            "params": {
                "fileName": f"{filename}",
                "file": recipients
            }
        }
        authorization = {"Authorization": token}

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            
            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()

                if openfin_content.get('ok'):
                    data = {
                        "status":True,
                        "detail": openfin_content.get('message'),
                        "mensaje": "Se guardo correctamente la importacion"
                    }
                    return data
                else:
                    data={
                        "status":False,
                        "detail":openfin_content.get('error'),
                        "mensaje":"No se pudo importar archivo en OpenFin"
                    }
                    return data


            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def list_imports(self,filename: str,token: str):
        """list the recipients"""
        openfin_data = {"detail": "El proveedor no respondio exitosamente"}

        data = {
          "recurso": "proveedores/listadoBenefImp",
          "params": {}
        }
        authorization = {"Authorization": token}

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                list_recipients = openfin_content["data"]
                for item in list_recipients:
                    if item.get('Archivo') == filename:
                        return item
                return None
            else:
                print(openfin_response.json())
                return openfin_data

        except Exception as error_exception:
            return openfin_data

    def show_imports(self,token: str):
        """list the recipients"""
        openfin_data = {"detail": "El proveedor no respondio exitosamente"}

        data = {
          "recurso": "proveedores/listadoBenefImp",
          "params": {}
        }
        authorization = {"Authorization": token}

        try:
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if openfin_response.status_code == 200:
                openfin_content = openfin_response.json()
                list_recipients = openfin_content["data"]
                return list_recipients
            else:
                print(openfin_response.json())
                return openfin_data

        except Exception as error_exception:
            return openfin_data

    def detail_import(self,id:int,token: str,):
        """
        Crea un destinatario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        authorization = {"Authorization": token}
        data={
          "recurso": "proveedores/benefImpDetalle",
          "params": {
            "id": int(id)
          }
        }
        # print(f"OPENFIN - data {data}")
        try:
            response_openfin = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            # print(f"OPENFIN - response {response_openfin.json()}")
            if response_openfin.status_code == 200:
                openfin_data_response= response_openfin.json()
                # print(f"OPENFIN - {response_openfin.json().get('data')}")
                if openfin_data_response.get('data'):

                    return openfin_data_response.get('data')
                else:
                    return None
            else:
                return None

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

    def apply_import(self, id: int, token: str, ):
        """
        Crea un destinatario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        authorization = {"Authorization": token}
        data = {
          "recurso": "proveedores/aplicarBenefImp",
          "params": {
            "idarchivo": id
          }
        }

        try:
            response_openfin = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if response_openfin.status_code == 200:
                openfin_data_response = response_openfin.json()

                if openfin_data_response.get('ok'):
                    data_response={
                        'status':True,
                        'detail':openfin_data_response.get('message')
                    }
                    return data_response
                else:
                    data_response = {
                        'status': False,
                        'detail': openfin_data_response.get('error')
                    }
                    return data_response
            else:
                return None

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

    def delete_import(self, id: int, token: str) -> any:
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        authorization = {"Authorization": token}
        data = {
            "recurso": "proveedores/deleteBenefImp",
            "params": {
                "idarchivo": id
            }
        }

        try:
            response_openfin = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if response_openfin.status_code == 200:
                openfin_data_response = response_openfin.json()

                if openfin_data_response.get('ok'):
                    data_response = {
                        'status': True,
                        'detail': openfin_data_response.get('message')
                    }
                    return data_response
                else:
                    data_response = {
                        'status': False,
                        'detail': openfin_data_response.get('error')
                    }
                    return data_response
            else:
                return None

        except Exception as error_exception:
            print(
                f"Error {error_exception} en la respuesta de openfin al crear destinatario"
            )
            return openfin_data

