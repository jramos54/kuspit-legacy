# Proyecto
from ..db_open_fin.repository_implementation_movement_openfin import (
    MovementsImplementation,
)
from ....engine.use_cases.ports.secondaries import repository_movement as repository


def constructor_movements() -> repository.MovementRepository:
    return MovementsImplementation()
