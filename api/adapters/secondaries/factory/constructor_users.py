from api.adapters.secondaries.db_orm.repository_implementation_users import (
    User as UserORM,
)
from api.engine.use_cases.ports.secondaries import repository_users as repository

# orm
from apps.backoffice.models import users as models_users


def constructor_users(users_orm_model: models_users.User) -> repository.UserDyPRepository:
    return UserORM(users_orm_model=users_orm_model)
