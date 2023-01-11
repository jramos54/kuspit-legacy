from api.engine.use_cases.ports.secondaries import (
    repository_user_secure_code as repository,
)
from api.engine.use_cases.factory import orm_mapper
from api.engine.domain.entities import entities_user_secure_code as entity
from apps.backoffice.models import users as models_users


class UserSecureCode(repository.UserSecureCodeRepository):
    def __init__(self, users_secure_code_orm_model: models_users.UserSecureCode):
        self._users_secure_code_orm_model = users_secure_code_orm_model

    def get_code(self, code: int) -> entity.UserSecureCode:
        user_code = self._users_secure_code_orm_model.objects.filter(
            code=code,
        ).last()
        return orm_mapper.constructor_user_secure_code_entities(user_code)

    def create_code(
        self,
        user_id: int,
        code: int,
        expedition_datetime: str,
        tries: int,
        is_active: bool,
    ) -> entity.UserSecureCode:
        user_code = self._users_secure_code_orm_model.objects.create(
            user_id=user_id,
            code=code,
            expedition_datetime=expedition_datetime,
            tries=tries,
            is_active=is_active,
        )
        return orm_mapper.constructor_user_secure_code_entities(user_code)

    def update_code(
        self,
        id: int,
        code: int,
        expedition_time: str,
        tries: int,
        is_active: bool,
    ) -> entity.UserSecureCode:
        user_code = self._users_secure_code_orm_model.objects.get(id=id)
        user_code.code = code if code else user_code.code
        user_code.expedition_datetime = (
            expedition_time if expedition_time else user_code.expedition_datetime
        )
        user_code.tries = tries if tries else user_code.tries
        user_code.is_active = is_active if is_active else user_code.is_active

        user_code.save(
            update_fields=[
                "code",
                "expedition_time",
                "tries",
                "is_active",
            ]
        )
        return orm_mapper.constructor_user_secure_code_entities(user_code)
