# Librerias Estandar
import abc

__all__ = [
    "PersonaMoral",
]


class PersonaMoral(abc.ABC):
    @abc.abstractmethod
    def create_persona_moral(self, info: dict) -> dict:
        ...

    # @abc.abstractmethod
    # def update_persona_moral(self,
    #                     info: dict,
    #                     id: int
    #                     ) -> dict:
    #     ...

    # @abc.abstractmethod
    # def get_persona_moral(self,
    #                     id: int,
    #                     ) -> None:
    #     ...
