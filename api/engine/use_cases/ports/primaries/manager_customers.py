# Librerias Estandar
import typing
import abc


class Customer(abc.ABC):
    @abc.abstractmethod
    def list_customers(self, *args, **kwargs) -> typing.List[dict]:
        ...
