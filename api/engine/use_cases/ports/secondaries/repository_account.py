"""secondary ports for engine accounts service"""
# Librerias Estandar
import typing
import abc

__all__ = [
    "Account",
]


class Account(abc.ABC):
    @abc.abstractmethod
    def create_account(
        self,
        alias: str,
        type_account: int,
        token: str,
    ) -> dict:
        ...

    @abc.abstractmethod
    def list_accounts(self, token: str) -> typing.List[dict]:
        ...

    @abc.abstractmethod
    def get_account(self, kauxiliar: int, token: str) -> dict:
        ...
