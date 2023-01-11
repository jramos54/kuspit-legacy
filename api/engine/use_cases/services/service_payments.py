# Librerias Estandar
import typing

from api.engine.use_cases.ports.secondaries import repository_payments as repository
from api.engine.use_cases.ports.primaries import manager_payments as manager
from api.engine.domain.entities import entities_payments as entity


class Payments(manager.Payments):
    def __init__(self, payments_repository: repository.Payments):
        self.payments_repository = payments_repository

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
        payment = self.payments_repository.create_payment(
            kauxiliar=kauxiliar,
            id_recipient=id_recipient,
            id_account=id_account,
            amount=amount,
            description=description,
            payment_date=payment_date,
            reference=reference,
            payment_hour=payment_hour,
            token=token,
        )
        return payment

    def list_payments(
        self, date: str, to_date: str, token: str
    ) -> typing.List[entity.PaymentsOpenFin]:
        payment = self.payments_repository.list_payments(
            date=date,
            to_date=to_date,
            token=token,
        )
        return payment

    def delete_payment(self, id_transaction: int, token: str) -> any:
        payment = self.payments_repository.delete_payment(
            id_transaction=id_transaction,
            token=token,
        )
        return payment

    def list_payments_manager(self, *args, **kwargs) -> typing.List[entity.Payments]:
        customer_id = kwargs.get("customer_id", None)

        if customer_id:
            return self.payments_repository.list_payments(customer_id=customer_id)

        return self.payments_repository.list_payments()
