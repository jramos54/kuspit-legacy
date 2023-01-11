# Librerias Estandar
import re

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_recipient as exceptions


class UserDashboardSerializer(serializers.Serializer):
    """Recipient Serializer"""

    nombre = serializers.CharField(max_length=50, required=False, allow_blank=True)
    correo = serializers.EmailField(required=False, allow_blank=True)
    kasociado = serializers.IntegerField(required=False,allow_null=True)
    # perfil = serializers.CharField(max_length=50, required=False, allow_blank=True)
    perfil = serializers.ListField(child=serializers.CharField(), required=False)
    status_2fa = serializers.BooleanField(required=False)


    def validate(self, attrs):
        """Validaciones"""
        if self.partial:
            return attrs

        return attrs
