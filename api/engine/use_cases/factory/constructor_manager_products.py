"""constructor manager for products engine"""
from api.engine.use_cases.ports.secondaries import repository_products as repository
from api.engine.use_cases.ports.primaries import manager_products as manager
from api.engine.use_cases.services import service_products as service


def constructor_manager_products(
    product_repository: repository.Product,
) -> manager.Product:
    """fuction to return the service of products"""
    return service.Product(product_repository)
