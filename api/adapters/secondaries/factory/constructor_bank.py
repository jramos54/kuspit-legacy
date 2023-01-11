# Proyecto
from ..db_open_fin.repository_implementation_bank_openfin import BankImplementation
from ....engine.use_cases.ports.secondaries import repository_bank as repository


def constructor_bank() -> repository.BankRepository:
    return BankImplementation()
