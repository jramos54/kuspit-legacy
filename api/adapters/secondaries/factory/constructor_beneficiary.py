# Proyecto
from ..db_open_fin.repository_implementation_beneficiary_openfin import BeneficiaryImpl
from ....engine.use_cases.ports.secondaries import repository_beneficiary as repository


def constructor_beneficiary() -> repository.Beneficiary:
    return BeneficiaryImpl()
