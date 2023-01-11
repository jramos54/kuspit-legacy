"""secondary port for products"""
# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_products as entity


class Product(abc.ABC):
    """
    ProductsRepository defines the methods that will use products
    """

    @abc.abstractmethod
    def list_products(self, token: str) -> typing.List[entity.Products]:
        ...

    @abc.abstractmethod
    def get_product(self, id_product: int, token: str) -> entity.Products:
        ...
