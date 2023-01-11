"""constructor for products"""
# Proyecto
# Proyecto
from ..db_open_fin.repository_implementation_products_openfin import ProductImpl
from ....engine.use_cases.ports.secondaries import repository_products as repository


def constructor_manager_products() -> repository.Product:
    return ProductImpl()
