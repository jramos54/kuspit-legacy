# Proyecto
from ....engine.use_cases.ports.secondaries import repository_customers as repository
from ....engine.use_cases.ports.primaries import manager_customers as manager
from ....engine.use_cases.services import service_customers as service


def constructor_manager_customers(
    customers_repository: repository.Customer,
) -> manager.Customer:
    return service.Customer(customers_repository=customers_repository)
