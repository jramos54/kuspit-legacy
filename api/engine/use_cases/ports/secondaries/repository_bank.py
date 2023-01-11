"""secondary port for bank"""
# librerias Estandar
# Librerias Estandar
import typing
import abc

# Proyecto
# proyecto
from ....domain.entities.entities_banks import Bank


class BankRepository(abc.ABC):
    """bank repository defines the method to be used"""

    @abc.abstractmethod
    def get_bank(self, nombre: str, token: str) -> Bank:
        ...

    def list_banks(self, token: str) -> typing.List[Bank]:
        ...
