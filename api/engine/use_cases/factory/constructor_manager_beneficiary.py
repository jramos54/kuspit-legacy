# Proyecto
from ..ports.secondaries import repository_beneficiary as repository
from ..ports.primaries import manager_beneficiary as manager
from ..services import service_beneficiary as service


def constructor_manager_beneficiary(
    beneficiary_repository: repository.Beneficiary,
) -> manager.Beneficiary:
    return service.Beneficiary(beneficiary_repository=beneficiary_repository)
