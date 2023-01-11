"""factory of bank"""

# proyecto
# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...use_cases import services as service


def constructor_manager_bank(
    bank_repository: repository.BankRepository,
) -> manager.BankManager:
    return service.BankService(bank_repository)
