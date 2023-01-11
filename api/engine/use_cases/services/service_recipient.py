"""Service for recipient"""
# Librerias Estandar
import typing

# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...domain.entities import entities_recipient as entity


class RecipientService(manager.RecipientManager):
    """RecipientService defines the methods"""

    def __init__(self, recipient_repository: repository.RecipientRepository):
        self.recipient_repository = recipient_repository

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
    ) -> entity.Recipient:
        """create a recipient"""
        recipient = self.recipient_repository.create_recipient(
            nombre=nombre,
            paterno=paterno,
            materno=materno,
            rfc=rfc,
            curp=curp,
            is_active=is_active,
            correo=correo,
            pfisica=pfisica,
            token=token,
        )
        return recipient

    def get_recipient(self, iddestinatario: int, token: str) -> entity.Recipient:
        """return a recipient by id"""

        recipient = self.recipient_repository.get_recipient(
            iddestinatario=iddestinatario, token=token
        )
        return recipient

    def list_recipient(self, token: str) -> typing.List[entity.Recipient]:
        """return a list of recipients"""
        recipients = self.recipient_repository.list_recipient(token=token)
        return recipients

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
    ) -> entity.Recipient:
        """Actualiza un destinatario"""

        recipient = self.recipient_repository.update_recipient(
            iddestinatario=iddestinatario,
            nombre=nombre,
            paterno=paterno,
            materno=materno,
            rfc=rfc,
            curp=curp,
            is_active=is_active,
            correo=correo,
            pfisica=pfisica,
            token=token,
        )
        return recipient

    def delete_recipient(self, iddestinatario: int, token: str) -> any:
        recipient = self.recipient_repository.delete_recipient(
            iddestinatario=iddestinatario, token=token
        )
        return recipient
