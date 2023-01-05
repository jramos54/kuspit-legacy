import typing
from api.engine.use_cases.ports.primaries import manager_customers as manager
from api.engine.use_cases.ports.secondaries import repository_customers as repository
from api.engine.domain.entities import entities_customers as entity


class Customer(manager.Customer):
    def __init__(self, customers_repository: repository.Customer):
        self.customers_repository = customers_repository

    def list_customers(self) -> typing.List[entity.Customer]:
        return self.customers_repository.list_customers()

    def get_customer(self, customer_id: int) -> entity.Customer:
        return self.customers_repository.get_customer(customer_id=customer_id)

    def create_customer(
        self,
        name: str,
        paternal_surname: str,
        email: str,
    ) -> entity.Customer:

        customer = self.customers_repository.create_customer(
            name=name,
            paternal_surname=paternal_surname,
            email=email,
        )
        return customer

    def update_customer(
        self,
        id: int,
        name: str,
        paternal_surname: str,
        email: str,
    ) -> entity.Customer:

        customer = self.customers_repository.update_customer(
            id=id,
            name=name,
            paternal_surname=paternal_surname,
            email=email,
        )
        return customer

    def delete_customer(
        self,
        id: int,
    ) -> None:

        self.customers_repository.delete_customer(
            id=id,
        )
        return None
