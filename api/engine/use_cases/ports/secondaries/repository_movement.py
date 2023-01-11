"""Manager for movement"""
# Librerias Estandar
import typing
import abc

# Proyecto
from ....domain.entities.entities_movement import Movement


class MovementRepository(abc.ABC):
    """Repository for  movement"""

    @abc.abstractmethod
    def list_movements_by_account(self, *args, **kwargs) -> typing.List[Movement]:
        ...
