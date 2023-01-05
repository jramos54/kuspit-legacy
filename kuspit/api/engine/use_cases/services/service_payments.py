import typing
from api.engine.use_cases.ports.primaries import manager_payments as manager
from api.engine.use_cases.ports.secondaries import repository_payments as repository
from api.engine.domain.entities import entities_payments as entity


class PaymentsCustomer(manager.PaymentsCustomer):
    def __init__(self, payments_repository: repository.PaymentsCustomer):
        self.payments_repository = payments_repository

    def list_payments(self,
                      *args,
                      **kwargs) -> typing.List[entity.PaymentsCustomer]:

        customer_id = kwargs.get('customer_id', None)

        if customer_id:
            return self.payments_repository.list_payments(customer_id=customer_id)
        else:
            return self.payments_repository.list_payments()
