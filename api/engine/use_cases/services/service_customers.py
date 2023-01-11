# Librerias Estandar
import typing

# Proyecto
from ....engine.use_cases.ports.secondaries import repository_customers as repository
from ....engine.use_cases.ports.primaries import manager_customers as manager


class Customer(manager.Customer):
    def __init__(self, customers_repository: repository.Customer):
        self.customers_repository = customers_repository

    def list_customers(self, *args, **kwargs) -> typing.List[dict]:
        return self.customers_repository.list_customers()
