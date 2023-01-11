"""secondary port for recipient"""
# Librerias Estandar
import abc

# Proyecto
from ....domain.entities.entities_recipient_accounts import RecipientAccount


class RecipientAccountRepository(abc.ABC):
    """
    RecipientRepository defines the methods that will use recipent
    """

    @abc.abstractmethod
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
    ) -> RecipientAccount:
        ...

    @abc.abstractmethod
    def update_recipient_account(
        self,
        idcuenta: int,
        is_active: bool,
        limite_operaciones: int,
        limite: float,
        alias: str,
        token: str,
    ) -> RecipientAccount:
        ...

    @abc.abstractmethod
    def delete_recipient_account(
        self, idcuenta: int, iddestinatario: int, token: str
    ) -> None:
        ...
