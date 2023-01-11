from api.adapters.secondaries.db_orm.repository_implementation_user_secure_code import (
    UserSecureCode as UserSecureCodeORM,
)
from api.engine.use_cases.ports.secondaries import (
    repository_user_secure_code as repository,
)
from apps.backoffice.models import users as models_users


def constructor_users_secure_code(
    users_secure_code_orm_model: models_users.UserSecureCode,
) -> repository.UserSecureCodeRepository:
    return UserSecureCodeORM(users_secure_code_orm_model=users_secure_code_orm_model)
