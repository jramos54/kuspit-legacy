# orm
from apps.backoffice.models import users as users_models

# Proyecto
from ....adapters.secondaries.db_orm.repository_implementation_customers import (
    Customer as CustomerORM,
)
from ....engine.use_cases.ports.secondaries import repository_customers as repository


def constructor_customers(
    customers_orm_model: users_models.User,
) -> repository.Customer:
    return CustomerORM(customers_orm_model=customers_orm_model)
