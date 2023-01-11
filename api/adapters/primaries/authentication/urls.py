# Librerías de Terceros
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path

# Proyecto
from .refresh_views import CustomTokenRefreshView
from .logout_views import LogoutView

urlpatterns = [
    path("logout", LogoutView.as_view(), name="logout"),
    path("login", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
