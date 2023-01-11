# Librerias Estandar
import typing

# Proyecto
from ...domain.entities.entities_movement import Movement
from ....engine.use_cases.ports import secondaries as repository
from ....engine.use_cases.ports import primaries as manager


class MovementService(manager.MovementManager):
    def __init__(self, movement_repository: repository.MovementRepository):
        self.movement_repository = movement_repository

    def list_movements_by_account(self, *args, **kwargs) -> typing.List[Movement]:
        movements = self.movement_repository.list_movements_by_account(*args, **kwargs)
        return movements
