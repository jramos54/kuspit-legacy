from api.engine.use_cases.ports.secondaries import repository_payments as repository
from api.engine.use_cases.ports.primaries import manager_payments as manager
from api.engine.use_cases.services import service_payments as service


def constructor_manager_payments(
    payments_repository: repository.Payments,
) -> manager.Payments:
    return service.Payments(payments_repository=payments_repository)
