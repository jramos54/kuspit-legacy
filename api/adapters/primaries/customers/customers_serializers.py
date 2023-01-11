# Librerías de Terceros
from rest_framework import serializers


class DomicilioSerializer(serializers.Serializer):
    """Serializer for domicilio info"""

    calle = serializers.CharField()
    numext = serializers.CharField()
    numint = serializers.CharField()
    pais = serializers.CharField()
    estado = serializers.CharField()
    ciudad = serializers.CharField()
    alcaldia = serializers.CharField()
    cp = serializers.CharField()
    # entrecalles = serializers.CharField()


class OtrosDatosPersonalesSerializer(serializers.Serializer):
    """Serializer for otros datos personales field"""

    numero_de_cuenta = serializers.IntegerField()
    clave_bancaria = serializers.IntegerField()
    institucion_financiera = serializers.CharField()
    nombre_comercial = serializers.CharField()
    actividades_y_otros = serializers.CharField()
    corroborar_datos = serializers.CharField()
    clave_bancaria_digitalizada = serializers.IntegerField()
    institucion_financiera_digitalizada = serializers.CharField()
    firma_digitalizada = serializers.CharField()


class QueryParamsCustomerSerializer(serializers.Serializer):
    """Serializer for Query Params Customer"""

    customer_id = serializers.IntegerField(required=False)
    openfin_id = serializers.IntegerField(required=False)
    payments_id = serializers.IntegerField(required=False)
    persona_fisica = serializers.BooleanField(required=False)
    persona_moral = serializers.BooleanField(required=False)


class BaseCustomerSerializer(serializers.Serializer):
    """Serializer for base customer"""

    id = serializers.IntegerField(required=False)
    is_persona_fisica = serializers.BooleanField()
    is_persona_moral = serializers.BooleanField()
