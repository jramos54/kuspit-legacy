# Proyecto
from ..db_open_fin.repository_implementation_movement_historical_openfin import (
    MovementsByMonthImplementation,
)
from ....engine.use_cases.ports.secondaries import (
    repository_movement_historical as repository,
)


def constructor_movements_historical() -> repository.MovementByMonthRepository:
    return MovementsByMonthImplementation()
