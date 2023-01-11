# Librerías de Terceros
from rest_framework import serializers


class MovementsByMonthSerializer(serializers.Serializer):
    mes = serializers.IntegerField(required=False, allow_null=True)
    depositos = serializers.DecimalField(
        required=False, max_digits=100, decimal_places=2, allow_null=True
    )
    retiros = serializers.DecimalField(
        required=False, max_digits=100, decimal_places=2, allow_null=True
    )
    pago_servicios = serializers.DecimalField(
        required=False, max_digits=100, decimal_places=2, allow_null=True
    )
    retiros_programados = serializers.DecimalField(
        required=False, max_digits=100, decimal_places=2, allow_null=True
    )
    current = serializers.BooleanField(required=False)


class QueryParamMovementsByMonthSerializer(serializers.Serializer):
    kauxiliar = serializers.IntegerField(required=False)
