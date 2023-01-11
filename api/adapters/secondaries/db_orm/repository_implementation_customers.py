# Librerias Estandar
import typing

# orm
from apps.backoffice.models import users as models_users

# Proyecto
# engine
from ....engine.use_cases.ports.secondaries import repository_customers as repository
from ....engine.use_cases.factory import orm_mapper
from ....engine.domain.entities import entities_users as entity

# from django.db import transaction


class Customer(repository.Customer):
    def __init__(self, customers_orm_model: models_users.User):
        self._customers_orm_model = customers_orm_model

    def list_customers(self, *args, **kwargs) -> typing.List[entity.UserDyP]:
        """
        List all customers
        :params:
            customer_id: int
            openfin_id: int
            payments_id: int
            persona_fisica: bool
            persona_moral: bool
        :return: list of customers
        """

        customer_id = kwargs.get("customer_id")
        openfin_id = kwargs.get("openfin_id")
        payments_id = kwargs.get("payments_id")
        persona_fisica = kwargs.get("persona_fisica")
        persona_moral = kwargs.get("persona_moral")

        # TODO: Validar que regrese solamente customers y no admins

        customers_queryset = models_users.User.objects.filter(
            is_customer=True, is_staff=False, is_superuser=False
        )

        if kwargs.get("customer_id"):
            customers_queryset = customers_queryset.get(id=customer_id)

        if kwargs.get("openfin_id"):
            customers_queryset = customers_queryset.get(open_fin_id=openfin_id)

        if kwargs.get("payments_id"):
            customers_queryset = customers_queryset.get(payments_user_id=payments_id)

        if kwargs.get("persona_fisica"):
            customers_queryset = customers_queryset.filter(
                is_persona_fisica=persona_fisica
            )
            # TODO: Implementar request a api de openfin y payments para obtener los datos de los usuarios

        if kwargs.get("persona_moral"):
            customers_queryset = customers_queryset.filter(
                is_persona_moral=persona_moral
            )
            # TODO: Implementar request a api de openfin y payments para obtener los datos de los usuarios

        customers_list = [
            orm_mapper.constructor_user_entities(customer)
            for customer in customers_queryset
        ]

        return customers_list
