# Librerías de Terceros
from django.urls import path

# Proyecto
from .user_dashboard_views import UserDashboardViewSet,UserNameViewSet


get_user_dashboard = {"get": "get_user_dashboard"}
get_user_by_email = {"get": "get_user_by_email"}
change_new_user={"patch":"change_new_user"}
update_status_2fa={"patch":"update_status_2fa"}


urlpatterns = [
    path(
        "dashboard",
        UserDashboardViewSet.as_view(
            {
                **get_user_dashboard,
            }
        ),
        name="dashboard",
    ),
    path(
            "dashboard/login",
            UserNameViewSet.as_view(
                {
                    **get_user_by_email,
                }
            ),
            name="nameUser",
        ),
    path(
            "dashboard/new-user",
            UserNameViewSet.as_view(
                {
                    **change_new_user,
                }
            ),
            name="newUser",
        ),
    path(
                "dashboard/status-2fa",
                UserDashboardViewSet.as_view(
                    {
                        **update_status_2fa,
                    }
                ),
                name="newUser",
            ),
]
