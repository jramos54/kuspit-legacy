# Librerias Estandar
import abc

__all__ = [
    "PersonaFisica",
]


class PersonaFisica(abc.ABC):
    @abc.abstractmethod
    def create_persona_fisica(self, info: dict) -> dict:
        ...

    # @abc.abstractmethod
    # def update_persona_fisica(self,
    #                     info: dict,
    #                     id: int
    #                     ) -> dict:
    #     ...

    # @abc.abstractmethod
    # def get_persona_fisica(self,
    #                     id: int,
    #                     ) -> None:
    #     ...
