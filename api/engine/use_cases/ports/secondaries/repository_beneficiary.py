# Librerias Estandar
import abc

__all__ = [
    "Beneficiary",
]


class Beneficiary(abc.ABC):
    @abc.abstractmethod
    def create_beneficiary(self, info: dict) -> dict:
        ...

    # @abc.abstractmethod
    # def update_beneficiary(self,
    #                     info: dict,
    #                     id: int
    #                     ) -> dict:
    #     ...

    # @abc.abstractmethod
    # def get_beneficiary(self,
    #                     id: int,
    #                     ) -> None:
    #     ...
