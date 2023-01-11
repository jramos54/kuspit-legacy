# Proyecto
from ....engine.use_cases.ports import secondaries as repository
from ....engine.use_cases.ports import primaries as manager
from ....engine.use_cases import services as service


def constructor_manager_movement_by_month(
    movement_by_month_repository: repository.MovementByMonthRepository,
) -> manager.MovementByMonthManager:
    return service.MovementByMonthService(
        movement_by_month_repository=movement_by_month_repository
    )
