# Librerías de Terceros
from django.urls import path

# Proyecto
from .spei_discount_views import SpeiDiscountViewSet


aplica_descuento = {"put": "aplica_descuento"}

urlpatterns = [
    path(
        "descuento-spei",
        SpeiDiscountViewSet.as_view(
            {
                **aplica_descuento,
            }
        ),
        name="aplicar-descuento",
    )
]
