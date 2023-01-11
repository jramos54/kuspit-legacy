# Proyecto
from ....engine.use_cases.ports import secondaries as repository
from ....engine.use_cases.ports import primaries as manager
from ....engine.use_cases import services as service


def constructor_manager_movement(
    movement_repository: repository.MovementRepository,
) -> manager.MovementManager:
    return service.MovementService(movement_repository=movement_repository)
