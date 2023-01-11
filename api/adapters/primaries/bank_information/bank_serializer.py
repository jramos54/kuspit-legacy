# Librerias
# Librerías de Terceros
from rest_framework import serializers


class BankSerializer(serializers.Serializer):
    key = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=255, required=False, allow_blank=True, help_text="Nombre comercial del banco")
    nombre_completo = serializers.CharField(
        max_length=255, required=False, allow_blank=True, help_text="Razon social del banco"
    )
    rfc = serializers.CharField(max_length=13, required=False, allow_blank=True)


class BankQueryParamsSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=False,help_text="Es el nombre del banco o parte del nombre")
    clabe = serializers.CharField(required=False,help_text="Es la cuenta clabe para identificar el banco")