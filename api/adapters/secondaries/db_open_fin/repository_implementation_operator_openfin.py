""" repository to conect to openfin"""
# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests
import typing

# Proyecto
from ....engine.domain.entities.entities_operadores import Operator, Permissions
from ....engine.use_cases.ports.secondaries import repository_operadores as repository
from .repository_implementation_user_dashboard_openfin import UserDashboardImplementation


class OperatorImplementation(repository.OperatorRepository):
    def __init__(self):
        self.url_listar_operadores = "http://" + OPENFIN_URL + "/rpc/operadores"
        self.url_acceso_operador = "http://" + OPENFIN_URL + "/rpc/operador_acceso"
        self.url_permisos_operador = "http://" + OPENFIN_URL + "/rpc/apife1"
        self.url_nuevo_operador = "http://" + OPENFIN_URL + "/rpc/operador_nuevo_temp"
        self.url_asignar_operador = "http://" + OPENFIN_URL + "/rpc/operador"

    def create_operator(self,
                        nombre: str,
                        paterno: str,
                        materno: str,
                        correo: str,
                        pfisica: bool,
                        password: str,
                        token: str) -> Operator:

        authorization = {"Authorization": token}
        try:
            kdir = self.new_operator(nombre=nombre, paterno=paterno, materno=materno, correo=correo, pfisica=pfisica,
                                     authorization=authorization)
            added = self.assign_operator(kdir=kdir, correo=correo, password=password, authorization=authorization)

            if added:
                print("operador creado")
                operators = self.list_operator(token)
                for operator in operators:
                    if operator.email == correo:
                        return operator
            else:
                data = {'detail': 'No se pudo agregar el operador a la cuenta'}
                return data
        except Exception as exception_data:
            print(exception_data)
            data = {'detail': 'Error al agregar el operador a la cuenta'}
            return  data

    def get_operator(self, idoperador: int, token: str) -> Operator:
        """get a operador by id"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {"datos": {"idoperador": idoperador}}
        authorization = {"Authorization": token}

        try:
            openfin_response_operador = requests.post(
                self.url_listar_operadores, json=data, headers=authorization
            )

            if openfin_response_operador.status_code == 200:
                # print(openfin_response_operador.json())
                operador_data = openfin_response_operador.json().get('data', [])
                print(f"GET_OPERATOR -openfin response : operator_data {operador_data}")
                if operador_data:
                    kasociado = operador_data[0].get('kasociado')

                    print(f"GET_OPERATOR -openfin response : kasociado {kasociado}")

                    permisos = self.get_role(kasociado, authorization)
                    print(f"get_operator, openfin {permisos}")
                    operador = Operator(
                        idoperador=operador_data[0].get('idoperador'),
                        kasociado=operador_data[0].get('kasociado'),
                        nombre=operador_data[0].get('nombre'),
                        email=operador_data[0].get('email'),
                        ingreso=operador_data[0].get('ingreso'),
                        acceso=operador_data[0].get('acceso'),
                        permisos=permisos
                    )
                    return operador

            else:
                openfin_data = openfin_response_operador.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la funcion get_operator: \n{error_exception}")
            return openfin_data

    def list_operator(self, token: str) -> typing.List[Operator]:
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {"datos": {}}
        authorization = {"Authorization": token}

        try:
            openfin_response_operador = requests.post(
                self.url_listar_operadores, json=data, headers=authorization
            )
            # print(f"IMPLEMENTATION OPENFIN: list Operator : openfin response {openfin_response_operador.json()}")
            if openfin_response_operador.status_code == 200:

                operador_data = openfin_response_operador.json().get('data', [])
                # print(f"IMPLEMENTATION OPENFIN: list Operator : openfin operador_data {operador_data}")

                if operador_data:
                    operadores = []
                    for member in operador_data:
                        # print(f"IMPLEMENTATION OPENFIN: list Operator : openfin member {member}")

                        kasociado = member.get('kasociado')
                        # print(f"IMPLEMENTATION OPENFIN: list Operator : openfin kasociado {kasociado}")

                        permisos = self.get_role(kasociado, authorization)
                        print(f"IMPLEMENTATION OPENFIN: list Operator : openfin permisos {permisos}")

                        operador = Operator(
                            idoperador=member.get('idoperador'),
                            kasociado=member.get('kasociado'),
                            nombre=member.get('nombre'),
                            email=member.get('email'),
                            ingreso=member.get('ingreso'),
                            acceso=member.get('acceso'),
                            permisos=permisos
                        )
                        operadores.append(operador)
                    return operadores

            else:
                openfin_data = openfin_response_operador.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin list operator: \n{error_exception}")
            return openfin_data

    def grant_access(self, idoperador: int, token: str) -> Operator:
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        data = {
            "datos": {
                "idoperador": idoperador
            }
        }
        authorization = {"Authorization": token}

        print(f"Authorization: {authorization}")
        print(f"Data: {data}")

        try:
            openfin_response_operador = requests.post(
                self.url_acceso_operador, json=data, headers=authorization
            )
            print(f"openfin_response_operador: {openfin_response_operador.json()}")
            if openfin_response_operador.status_code == 200:
                print(f"OPENFIN ACCESO OPERADOR {openfin_response_operador.json()}")
                operador = self.get_operator(idoperador=idoperador, token=token)
                return operador

            else:
                openfin_response = openfin_response_operador.json()
                return openfin_response

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def assign_role(self, idoperador: int, perfil: str, token: str) -> Operator:
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        operador = self.get_operator(idoperador=idoperador, token=token)
        kasociado = operador.kasociado

        data = {
            "recurso": "operadores/insertPermiso",
            "params": {
                "kasociado": kasociado,
                "idperfil": perfil
            }
        }
        authorization = {"Authorization": token}

        try:
            openfin_response_operador = requests.post(
                self.url_permisos_operador, json=data, headers=authorization
            )

            if openfin_response_operador.status_code == 200:
                operador_data = openfin_response_operador.json()
                if operador_data.get('ok', False):
                    operador = self.get_operator(idoperador=idoperador, token=token)
                    return operador
                else:
                    return operador_data

            else:
                openfin_data = openfin_response_operador.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def revoke_role(self, idoperador: int, perfil: str, token: str) -> Operator:
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}

        operador = self.get_operator(idoperador=idoperador, token=token)
        kasociado = operador.kasociado

        data = {
            "recurso": "operadores/deletePermiso",
            "params": {
                "kasociado": kasociado,
                "idperfil": perfil
            }
        }
        authorization = {"Authorization": token}

        try:
            openfin_response_operador = requests.post(
                self.url_permisos_operador, json=data, headers=authorization
            )

            if openfin_response_operador.status_code == 200:
                operador_data = openfin_response_operador.json()
                if operador_data.get('ok', False):
                    operador = self.get_operator(idoperador=idoperador, token=token)
                    return operador
                else:
                    return operador_data

            else:
                openfin_data = openfin_response_operador.json()
                return openfin_data

        except Exception as error_exception:
            print(f"Error en la respuesta de openfin: \n{error_exception}")
            return openfin_data

    def get_role(self, kasociado: int, authorization: dict):
        permisos_paylod = {
            "recurso": "operadores/permisos",
            "params": {
                "kasociado": kasociado
            }
        }

        openfin_response_permisos = requests.post(self.url_permisos_operador, json=permisos_paylod,
                                                  headers=authorization)
        print(f"get_role - OPENFIN : openfin_response_permisos {openfin_response_permisos.json()}")

        if openfin_response_permisos.status_code == 200:
            role_response = openfin_response_permisos.json()
            if role_response.get('data'):
                roles = role_response.get('data', [])
                for role in roles:
                    if role.get('Activo'):
                        return Permissions(perfil=role.get('Perfil', ''), descripcion=role.get('Descripción', ''))

                return Permissions(perfil='Sin_Perfil', descripcion='Operador sin perfil asignado')

            return Permissions(perfil='Sin_Acceso', descripcion='Operador sin Acceso a la cuenta')

    def new_operator(self, nombre: str, paterno: str, materno: str, correo: str, pfisica: bool, authorization: dict):
        data = {
            "datos": {
                "pfisica": pfisica,
                "nombre": nombre,
                "paterno": paterno,
                "materno": materno,
                "correo": correo
            }
        }

        openfin_new_operator = requests.post(self.url_nuevo_operador, json=data,
                                             headers=authorization)
        if openfin_new_operator.status_code == 200:
            operator_response = openfin_new_operator.json()
            if operator_response.get('data'):
                kdir = operator_response.get('data', []).get('kdir')
                return kdir

    def assign_operator(self, kdir: int, correo: str, password: str, authorization: dict):
        from ....adapters.secondaries.factory import (
            constructor_user_dashboard as user_dashboard_repository,
        )
        from ....engine.use_cases.factory import (
            constructor_manager_user_dashboard as user_dashboard_engine,
        )

        users_dashboard_repository = user_dashboard_repository.constructor_user_dashboard()
        users_dashboard_engine = user_dashboard_engine(users_dashboard_repository)

        bearer_token=authorization.get('Authorization')
        # token=bearer_token.strip('Bearer ')
        # print(token)
        dashboard_response=users_dashboard_engine.get_user_dashboard(token=bearer_token)
        kasociado=dashboard_response.kasociado

        data = {
            "datos": {
                "kasociado": kasociado,
                "kdir_operador": kdir,
                "email": correo,
                "password": password,
                "confirma": password
            }
        }

        openfin_assign_operator = requests.post(self.url_asignar_operador, json=data,
                                                headers=authorization)

        if openfin_assign_operator.status_code == 200:
            assign_response = openfin_assign_operator.json()
            if assign_response.get('code') == '0':
                return True

            return False
