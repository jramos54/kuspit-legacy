import abc
import typing
from api.engine.domain.entities import entities_customers as entity

__all__ = [
    'Customer',
]


class Customer(abc.ABC):

    @abc.abstractmethod
    def list_customers(self) -> typing.List[entity.Customer]:
        ...

    @abc.abstractmethod
    def create_customer(self,
                        name: str,
                        paternal_surname: str,
                        email: str,
                        ) -> entity.Customer:
        ...

    @abc.abstractmethod
    def update_customer(self,
                        id: int,
                        name: str,
                        paternal_surname: str,
                        email: str,
                        ) -> entity.Customer:
        ...

    @abc.abstractmethod
    def delete_customer(self,
                        id: int,
                        ) -> None:
        ...
