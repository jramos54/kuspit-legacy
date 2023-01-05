import abc
import typing
# from datatime import datatime
from api.engine.domain.entities import entities_payments as entity


class PaymentsCustomer(abc.ABC):

    @abc.abstractmethod
    def list_payments(self,
                      *args,
                      **kwargs
                      ) -> typing.List[entity.PaymentsCustomer]:
        ...

