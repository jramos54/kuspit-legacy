# Proyecto
from ..db_open_fin.repository_implementation_emails_openfin import (
    EmailNotificationImplementation,
)


def constructor_user_dashboard() -> EmailNotificationImplementation:
    return EmailNotificationImplementation()
