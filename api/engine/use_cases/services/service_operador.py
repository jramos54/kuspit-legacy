"""Service for recipient"""
# Librerias Estandar
import typing

# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...domain.entities import entities_operadores as entity


class OperatorService(manager.OperatorManager):
    """ defines the methods"""

    def __init__(self, operator_repository: repository.OperatorRepository):
        self.operator_repository = operator_repository

    def create_operator(self,
                        nombre:str,
                        paterno:str,
                        materno:str,
                        correo:str,
                        pfisica:bool,
                        password: str,
                        token:str) -> entity.Operator:
        operator=self.operator_repository.create_operator(
            nombre=nombre,
            paterno=paterno,
            materno=materno,
            correo=correo,
            pfisica=pfisica,
            password=password,
            token=token
            )
        return operator

    def get_operator(self, idoperador: int, token: str) -> entity.Operator:

        operator = self.operator_repository.get_operator(
            idoperador=idoperador, token=token
        )
        return operator

    def list_operator(self, token: str) -> typing.List[entity.Operator]:
        operatores = self.operator_repository.list_operator(token=token)
        return operatores

    def grant_access(self, idoperador: int, token: str) -> entity.Operator:
        operator = self.operator_repository.grant_access(
            idoperador=idoperador, token=token
        )
        return operator

    def assign_role(self, idoperador: int, perfil: str, token: str) -> entity.Operator:
        operator = self.operator_repository.assign_role(
            idoperador=idoperador, perfil=perfil,token=token
        )
        return operator

    def revoke_role(self, idoperador: int, perfil: str, token: str) -> entity.Operator:
        operator = self.operator_repository.revoke_role(
            idoperador=idoperador, perfil=perfil,token=token
        )
        return operator
