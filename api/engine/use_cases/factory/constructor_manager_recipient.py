"""factory of recipient"""
# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...use_cases import services as service


def constructor_manager_recipient(
    recipient_repository: repository.RecipientRepository,
) -> manager.RecipientManager:
    return service.RecipientService(recipient_repository)
