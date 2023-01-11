# Proyecto
from ..ports.secondaries import repository_beneficiary as repository
from ..ports.primaries import manager_beneficiary as manager


class Beneficiary(manager.Beneficiary):
    def __init__(self, beneficiary_repository: repository.Beneficiary):
        self.beneficiary_repository = beneficiary_repository

    def create_beneficiary(
        self,
        info: dict,
    ) -> dict:
        beneficiary = self.beneficiary_repository.create_beneficiary(
            info=info,
        )
        return beneficiary

    # def update_beneficiary(
    #         self,
    #         info: dict,
    #         id: int
    # ) -> dict:
    #     beneficiary = self.beneficiary_repository.update_beneficiary(
    #         info=info,
    #         id=id
    #     )
    #
    #     return beneficiary
    #
    # def get_beneficiary(
    #         self,
    #         id: int
    # ) -> dict:
    #     beneficiary = self.beneficiary_repository.get_beneficiary(
    #         id=id
    #     )
    #     return beneficiary
