import abc
import typing
from api.engine.domain.entities import entities_payments as entity

__all__ = [
    'PaymentsCustomer',
]


class PaymentsCustomer(abc.ABC):

    @abc.abstractmethod
    def list_payments(self,
                      *args,
                      **kwargs) -> typing.List[entity.PaymentsCustomer]:
        ...
