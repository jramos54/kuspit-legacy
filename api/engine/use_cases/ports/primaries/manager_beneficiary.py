# Librerias Estandar
import abc


class Beneficiary(abc.ABC):
    """
    ManagerBeneficiary is the interface that defines the methods that will use beneficiary
    """

    @abc.abstractmethod
    def create_beneficiary(self, info: dict) -> dict:
        ...

    # @abc.abstractmethod
    # def update_beneficiary(self, info: dict, id:int) -> dict:
    #     ...

    # @abc.abstractmethod
    # def get_beneficiary(self, id: int) -> dict:
    #     ...
