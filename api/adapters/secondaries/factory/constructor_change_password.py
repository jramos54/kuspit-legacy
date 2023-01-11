# Proyecto
from ..db_open_fin.repository_implementation_change_password import (
    ChangePasswordImplementation,
)


def constructor_change_password() -> ChangePasswordImplementation:
    return ChangePasswordImplementation()
