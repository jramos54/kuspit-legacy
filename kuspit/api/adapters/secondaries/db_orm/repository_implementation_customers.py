import typing

# engine
from api.engine.use_cases.ports.secondaries import repository_customers as repository
from api.engine.use_cases.factory import orm_mapper
from api.engine.domain.entities import entities_customers as entity

# orm
from apps.webApp.models import customers as models_customers
# from django.db import transaction


class Customer(repository.Customer):
    def __init__(self, customers_orm_model: models_customers.Customer):
        self._customers_orm_model = customers_orm_model

    def list_customers(self) -> typing.List[entity.Customer]:
        return [
            orm_mapper.constructor_customer_entities(customer)
            for customer in self._customers_orm_model.objects.all()
        ]

    def get_customer(self, customer_id: int) -> entity.Customer:

        customer = self._customers_orm_model.objects.get(id=customer_id)
        return orm_mapper.constructor_customer_entities(customer)

    def create_customer(
        self,
        name: str,
        paternal_surname: str,
        email: str,
    ) -> entity.Customer:
        customer = self._customers_orm_model.objects.create(
            name=name,
            paternal_surname=paternal_surname,
            email=email,
        )

        return orm_mapper.constructor_customer_entities(customer)

    def update_customer(
        self,
        id: int,
        name: str,
        paternal_surname: str,
        email: str,
    ) -> entity.Customer:
        customer = self._customers_orm_model.objects.get(id=id)
        customer.name = name
        customer.paternal_surname = paternal_surname
        customer.email = email
        customer.save(update_fields=["name", "paternal_surname", "email"])

        return orm_mapper.constructor_customer_entities(customer)

    def delete_customer(self, id: int) -> None:
        customer = self._customers_orm_model.objects.get(id=id)
        customer.delete()
