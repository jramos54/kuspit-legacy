import typing
import abc

# Proyecto
from ....domain.entities.entities_operadores import Operator,Permissions

class OperatorManager(abc.ABC):

    @abc.abstractmethod
    def create_operator(self,
                        nombre:str,
                        paterno:str,
                        materno:str,
                        correo:str,
                        pfisica:bool,
                        password:str,
                        token:str) -> Operator:
        ...

    @abc.abstractmethod
    def get_operator(self,idoperador:int,token:str)->Operator:
        ...

    @abc.abstractmethod
    def list_operator(self,token:str)->typing.List[Operator]:
        ...

    @abc.abstractmethod
    def grant_access(self,idoperador:int,token:str):
        ...

    @abc.abstractmethod
    def assign_role(self,idoperador:int,perfil: str,token:str):
        ...

    @abc.abstractmethod
    def revoke_role(self,idoperador:int,perfil: str,token:str):
        ...

