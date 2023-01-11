# Librerias Estandar
import abc


class PersonaFisica(abc.ABC):
    """
    ManagerPersonaFisica is the interface that defines the methods that will use personafisica
    """

    @abc.abstractmethod
    def create_persona_fisica(self, info: dict) -> dict:
        ...

    # @abc.abstractmethod
    # def update_persona_fisica(self, info: dict, id:int) -> dict:
    #     ...

    # @abc.abstractmethod
    # def get_persona_fisica(self, id: int) -> dict:
    #     ...
