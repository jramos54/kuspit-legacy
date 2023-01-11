# Proyecto
from ..db_open_fin.repository_implementation_account_openfin import AccountImpl
from ....engine.use_cases.ports.secondaries import repository_account as repository


def constructor_manager_account() -> repository.Account:
    return AccountImpl()
