"""secondary ports for engine payments service"""
# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_payments as entity

__all__ = [
    "Payments",
]


class Payments(abc.ABC):
    @abc.abstractmethod
    def create_payment(
        self,
        kauxiliar: int,
        id_recipient: int,
        id_account: int,
        amount: float,
        description: str,
        payment_date: str,
        reference: str,
        payment_hour: str,
        token: str,
    ) -> entity.Payments:
        ...

    @abc.abstractmethod
    def list_payments(
        self, date: str, to_date: str, token: str
    ) -> typing.List[entity.PaymentsOpenFin]:
        ...

    @abc.abstractmethod
    def delete_payment(self, id_transaction: int, token: str) -> any:
        ...
