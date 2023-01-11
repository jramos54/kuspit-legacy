# Librerias Estandar
import abc


class PersonaMoral(abc.ABC):
    """
    ManagerPersonaFisica is the interface that defines the methods that will use personafisica
    """

    @abc.abstractmethod
    def create_persona_moral(self, info: dict) -> dict:
        """
        create_persona_moral is the method that will create a persona moral
        """

        # @abc.abstractmethod
        # def update_persona_moral(self, info: dict, id:int) -> dict:
        #     ...

        # @abc.abstractmethod
        # def get_persona_moral(self, id: int) -> dict:
