# Librerías de Terceros
from rest_framework import serializers


class BeneficiarySerializer(serializers.Serializer):
    """Benificiary Serializer"""

    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()
    fecha_nacimiento = serializers.DateField()
    calle = serializers.CharField()
    numext = serializers.CharField()
    numint = serializers.CharField()
    pais = serializers.CharField()
    estado = serializers.CharField()
    ciudad = serializers.CharField()
    alcaldia = serializers.CharField()
    cp = serializers.CharField()
    parentesco = serializers.CharField()
    porcentaje = serializers.FloatField()


class BeneficiaryQueryParamSerializer(serializers.Serializer):
    # limit = serializers.IntegerField()
    openfin_id = serializers.IntegerField(required=False)
    idasociado = serializers.IntegerField(required=False)
