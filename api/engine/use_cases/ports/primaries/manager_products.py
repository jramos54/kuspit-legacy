"""primary  port for products"""
# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_products as entity


class Product(abc.ABC):
    """
    Manager Product is the interface that defines the methods that will use products service
    """

    @abc.abstractmethod
    def list_products(self, token: str) -> typing.List[entity.Products]:
        ...

    @abc.abstractmethod
    def get_product(self, id_product: int, token: str) -> entity.Products:
        ...
