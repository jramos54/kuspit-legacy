# Proyecto
from .....compartidos.exceptions import ExceptionBase


class BeneficiaryDoesNotExist(ExceptionBase):
    """Beneficiary does not exist"""

    def __init__(self, beneficiary_id: int):
        self.beneficiary_id = beneficiary_id
        self.message = {"detail": f"Beneficiary {self.beneficiary_id} does not exist"}


class BeneficiaryAlreadyExist(ExceptionBase):
    """Beneficiary already exist"""

    def __init__(self, beneficiary_id: str):
        self.beneficiary_id = beneficiary_id
        self.message = {
            "detail": f"Beneficiary with id: {self.beneficiary_id} is already assigned to another beneficiary"
        }
