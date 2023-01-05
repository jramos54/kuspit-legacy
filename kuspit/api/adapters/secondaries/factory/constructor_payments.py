from api.adapters.secondaries.db_orm.repository_implementation_payments import PaymentsCustomer as PaymentsCustomerORM
from api.engine.use_cases.ports.secondaries import repository_payments as repository

# orm
from apps.webApp.models import customers as models_customers


def constructor_payments(payments_orm_model: models_customers.PaymentsCustomer) -> repository.PaymentsCustomer:
    return PaymentsCustomerORM(
        payments_orm_model=payments_orm_model
    )
