# librerias
# Librerías de Terceros
from django.urls import path

# Proyecto
from .bank_views import BanksViewSet

list_banks = {"get": "list_banks"}

urlpatterns = [path("bank", BanksViewSet.as_view({**list_banks}), name="bank")]
