# Proyecto
from ..db_open_fin.repository_implementation_password_recovery_openfin import (
    PasswordRecoveryImplementation,
)


def constructor_user_dashboard() -> PasswordRecoveryImplementation:
    return PasswordRecoveryImplementation()
