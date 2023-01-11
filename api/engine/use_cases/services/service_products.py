"""Service for products"""
# Librerias Estandar
# Librerias Estandar
import typing

from api.engine.use_cases.ports.secondaries import repository_products as repository
from api.engine.use_cases.ports.primaries import manager_products as manager
from api.engine.domain.entities import entities_products as entity


class Product(manager.Product):
    """ProductService defines the methods"""

    def __init__(self, product_repository: repository.Product):
        self.product_repository = product_repository

    def list_products(self, token: str) -> typing.List[entity.Products]:
        """return a list of products"""
        product = self.product_repository.list_products(token=token)
        return product

    def get_product(self, id_product: int, token: str) -> entity.Products:
        """return a product by id"""
        product = self.product_repository.get_product(
            id_product=id_product, token=token
        )
        return product
