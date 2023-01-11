# Proyecto
from ..db_open_fin.repository_implementation_operator_openfin import (
    OperatorImplementation,
)
from ....engine.use_cases.ports.secondaries import repository_operadores as repository


def constructor_operator() -> repository.OperatorRepository:
    return OperatorImplementation()
