# engine
# from api.engine.use_cases.ports import primaries
import typing

from api.engine.use_cases.ports.secondaries import repository_payments as repository
from api.engine.use_cases.factory import orm_mapper
from api.engine.domain.entities import entities_payments as entity

# orm
from apps.webApp.models import customers as models_customers


class PaymentsCustomer(repository.PaymentsCustomer):
    def __init__(self, payments_orm_model: models_customers.PaymentsCustomer):
        self._payments_orm_model = payments_orm_model

    def list_payments(self,
                      *args,
                      **kwargs) -> typing.List[entity.PaymentsCustomer]:

        customer_id = kwargs.get('customer_id', None)

        if customer_id is None:
            return [
                orm_mapper.constructor_payment_entities(payment)
                for payment in self._payments_orm_model.objects.all()
            ]

        else:
            return [
                orm_mapper.constructor_payment_entities(payment)
                for payment in self._payments_orm_model.objects.filter(
                    customer_id=customer_id
                )
            ]
