"""Service for recipient"""
# Librerias Estandar

# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...domain.entities import entities_recipient_accounts as entity


class RecipientAccountService(manager.RecipientAccountManager):
    """RecipientService defines the methods"""

    def __init__(
        self, recipient_account_repository: repository.RecipientAccountRepository
    ):
        self.recipient_account_repository = recipient_account_repository

    def create_recipient_account(
        self,
        iddestinatario: int,
        cuenta: int,
        institucion_bancaria: str,
        catalogo_cuenta: str,
        is_active: bool,
        limite_operaciones: int,
        limite: float,
        alias: str,
        token: str,
    ) -> entity.RecipientAccount:
        """create a recipient account"""
        recipient_account = self.recipient_account_repository.create_recipient_account(
            iddestinatario=iddestinatario,
            cuenta=cuenta,
            institucion_bancaria=institucion_bancaria,
            catalogo_cuenta=catalogo_cuenta,
            is_active=is_active,
            limite_operaciones=limite_operaciones,
            limite=limite,
            alias=alias,
            token=token,
        )
        return recipient_account

    def update_recipient_account(
        self,
        idcuenta: int,
        is_active: bool,
        limite_operaciones: int,
        limite: float,
        alias: str,
        token: str,
    ) -> entity.RecipientAccount:
        """Actualiza un destinatario"""

        recipient_account = self.recipient_account_repository.update_recipient_account(
            idcuenta=idcuenta,
            is_active=is_active,
            limite_operaciones=limite_operaciones,
            limite=limite,
            alias=alias,
            token=token,
        )
        return recipient_account

    def delete_recipient_account(
        self, idcuenta: int, iddestinatario: int, token: str
    ) -> any:
        delete_account = self.recipient_account_repository.delete_recipient_account(
            idcuenta=idcuenta, iddestinatario=iddestinatario, token=token
        )
        return delete_account
