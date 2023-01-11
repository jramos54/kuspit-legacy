from api.engine.use_cases.ports.secondaries import (
    repository_user_secure_code as repository,
)
from api.engine.use_cases.ports.primaries import manager_user_secure_code as manager
from api.engine.domain.entities import entities_user_secure_code as entity


class UserSecureCodeService(manager.UserSecureCodeManager):
    def __init__(
        self, user_secure_code_repository: repository.UserSecureCodeRepository
    ):
        self.user_secure_code_repository = user_secure_code_repository

    def get_code(self, code: int) -> entity.UserSecureCode:
        return self.user_secure_code_repository.get_code(code=code)

    def create_code(
        self,
        user_id: int,
        code: int,
        expedition_datetime: str,
        tries: int,
        is_active: bool,
    ) -> entity.UserSecureCode:
        secure_code = self.user_secure_code_repository.create_code(
            user_id=user_id,
            code=code,
            expedition_datetime=expedition_datetime,
            tries=tries,
            is_active=is_active,
        )
        return secure_code

    def update_code(
        self, id: int, user_id: int, code: int, expedition_datetime: str, tries: int
    ) -> entity.UserSecureCode:
        secure_code = self.user_secure_code_repository.update_code(
            id=id,
            user_id=user_id,
            code=code,
            expedition_datetime=expedition_datetime,
            tries=tries,
        )
        return secure_code
