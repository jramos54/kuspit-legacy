# Proyecto
from ..db_open_fin.repository_implementation_payments_openfin import PaymentsImpl
from ....engine.use_cases.ports.secondaries import repository_payments as repository


def constructor_manager_payments() -> repository.Payments:
    return PaymentsImpl()
