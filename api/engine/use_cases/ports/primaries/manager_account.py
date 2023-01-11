"""primary ports for engine accounts service"""
# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_accounts as entity


class Account(abc.ABC):
    """
    ManagerAccount is the interface that defines the methods that will use accounts
    """

    @abc.abstractmethod
    def create_account(
        self,
        alias: str,
        type_account: int,
        token: str,
    ) -> entity.Accounts:
        ...

    @abc.abstractmethod
    def list_accounts(self, token: str) -> typing.List[entity.Accounts]:
        ...

    @abc.abstractmethod
    def get_account(self, kauxiliar: int, token: str) -> entity.Accounts:
        ...
