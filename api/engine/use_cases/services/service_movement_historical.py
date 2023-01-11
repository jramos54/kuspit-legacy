# Librerias Estandar
import typing

# Proyecto
from ...domain.entities.entities_movement_historical import MovementByMonth
from ....engine.use_cases.ports import secondaries as repository
from ....engine.use_cases.ports import primaries as manager


class MovementByMonthService(manager.MovementByMonthManager):
    def __init__(
        self, movement_by_month_repository: repository.MovementByMonthRepository
    ):
        self.movement_by_month_repository = movement_by_month_repository

    def list_movements_by_month(self, *args, **kwargs) -> typing.List[MovementByMonth]:
        movements = self.movement_by_month_repository.list_movements_by_month(
            *args, **kwargs
        )
        return movements
