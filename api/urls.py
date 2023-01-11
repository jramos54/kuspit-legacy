# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from drf_yasg.views import get_schema_view
from django.urls import re_path, include, path
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DyP API",
        default_version="v1",
        description="Esta api es para el sistema de pagos DyP",
    ),
    public=True,
    permission_classes=[DjangoModelPermissions],
    # authentication_classes=[IsAuthenticated],
)

urlpatterns = [
    # path("", include("api.adapters.primaries.customers.urls")),
    path("", include("api.adapters.primaries.accounts.urls")),
    path("", include("api.adapters.primaries.payments.urls")),
    path("", include("api.adapters.primaries.users.urls")),
    path("", include("api.adapters.primaries.recipients.urls")),
    # path("", include("api.adapters.primaries.beneficiary.urls")),
    # path("", include("api.adapters.primaries.documents.urls")),
    path("", include("api.adapters.primaries.authentication.urls")),
    path("", include("api.adapters.primaries.movements.urls")),
    path("", include("api.adapters.primaries.authentication.urls")),
    path("", include("api.adapters.primaries.frequent_questions.urls")),
    path("", include("api.adapters.primaries.bank_information.urls")),
    path("", include("api.adapters.primaries.recipients_accounts.urls")),
    path("", include("api.adapters.primaries.products.urls")),
    path("", include("api.adapters.primaries.movements_historical.urls")),
    path("", include("api.adapters.primaries.user_dashboard.urls")),
    path("", include("api.adapters.primaries.operadores.urls")),
    path("", include("api.adapters.primaries.recovery_password.urls")),
    path("", include("api.adapters.primaries.recipients_batch.urls")),
    path("", include("api.adapters.primaries.payments_batch.urls")),
    path("", include("api.adapters.primaries.change_password.urls")),
    path("", include("api.adapters.primaries.spei_discount.urls")),

    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
