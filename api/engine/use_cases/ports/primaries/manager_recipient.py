"""primary port for recipient"""
# Librerias Estandar
import typing
import abc

# Proyecto
from ....domain.entities.entities_recipient import Recipient


class RecipientManager(abc.ABC):
    """
    ManagerRecipient defines the methods that will use recipent
    """

    @abc.abstractmethod
    def create_recipient(
        self,
        nombre: str,
        paterno: str,
        materno: str,
        rfc: str,
        curp: str,
        is_active: bool,
        correo: str,
        pfisica: bool,
        token: str,
    ) -> Recipient:
        ...

    @abc.abstractmethod
    def get_recipient(self, iddestinatario: int, token: str) -> Recipient:
        ...

    @abc.abstractmethod
    def list_recipient(self, token: str) -> typing.List[Recipient]:
        ...

    @abc.abstractmethod
    def update_recipient(
        self,
        iddestinatario: int,
        nombre: str,
        paterno: str,
        materno: str,
        rfc: str,
        curp: str,
        is_active: bool,
        correo: str,
        pfisica: bool,
        token: str,
    ) -> Recipient:
        ...

    @abc.abstractmethod
    def delete_recipient(self, iddestinatario: int, token: str) -> any:
        ...
