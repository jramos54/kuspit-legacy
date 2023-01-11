"""service for bank"""
# Librerias estandar
# Librerias Estandar
import typing

# Proyecto
# proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...domain.entities import entities_banks as entity


class BankService(manager.BankManager):
    """bankservice defines the methods to be used"""

    def __init__(self, bank_repository: repository.BankRepository):
        self.bank_repository = bank_repository

    def get_bank(self, nombre: str, token: str) -> entity.Bank:
        bank = self.bank_repository.get_bank(nombre=nombre, token=token)
        return bank

    def list_banks(self, token: str) -> typing.List[entity.Bank]:
        list_bank = self.bank_repository.list_banks(token=token)
        return list_bank
