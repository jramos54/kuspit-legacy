"""products urls"""
# Librerías de Terceros
from django.urls import path

# Proyecto
from .products_views import ProductsViewSet

# products
list_products = {"get": "list_products"}

urlpatterns = [
    path(
        "products",
        ProductsViewSet.as_view(
            {
                **list_products,
            }
        ),
        name="products",
    ),
]
