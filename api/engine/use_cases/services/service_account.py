# Librerias Estandar
import typing

from api.engine.use_cases.ports.secondaries import repository_account as repository
from api.engine.use_cases.ports.primaries import manager_account as manager
from api.engine.domain.entities import entities_accounts as entity


class Account(manager.Account):
    def __init__(self, account_repository: repository.Account):
        self.account_repository = account_repository

    def create_account(
        self,
        alias: str,
        type_account: int,
        token: str,
    ) -> entity.Accounts:
        account = self.account_repository.create_account(
            alias=alias,
            type_account=type_account,
            token=token,
        )
        return account

    def list_accounts(self, token: str) -> typing.List[entity.Accounts]:
        account = self.account_repository.list_accounts(
            token=token,
        )
        return account

    def get_account(self, kauxiliar: int, token: str) -> entity.Accounts:
        account = self.account_repository.get_account(kauxiliar=kauxiliar, token=token)
        return account
