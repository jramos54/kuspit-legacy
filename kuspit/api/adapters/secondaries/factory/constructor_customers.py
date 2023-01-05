from api.adapters.secondaries.db_orm.repository_implementation_customers import Customer as CustomerORM
from api.engine.use_cases.ports.secondaries import repository_customers as repository

# orm
from apps.webApp.models import customers as models_customers


def constructor_customers(customers_orm_model: models_customers.Customer) -> repository.Customer:
    return CustomerORM(
        customers_orm_model=customers_orm_model
    )
