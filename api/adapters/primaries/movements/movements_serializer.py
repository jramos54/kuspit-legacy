# Librerías de Terceros
from rest_framework import serializers


class MovementsSerializer(serializers.Serializer):
    fecha_elaboracion = serializers.DateField(
        format="%Y-%M-%D", required=False, allow_null=True
    )
    fecha_pago = serializers.DateField(
        format="%Y-%M-%D", required=False, allow_null=True
    )
    movimiento = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    estatus = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    destinatario = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    cuenta_bancaria = serializers.CharField(required=False, allow_null=True)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    concepto = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    clave_rastreo = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    referencia = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    info = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pfisica= serializers.BooleanField(required=False, allow_null=True)
    institucion_bancaria= serializers.CharField(required=False, allow_null=True, allow_blank=True)


class QueryParamMovementsSerializer(serializers.Serializer):
    kauxiliar = serializers.IntegerField(required=False, help_text="es el codigo de la wallet que se requiere consultar")
    defecha = serializers.DateField(format="%Y-%m-%d", required=False, help_text="se especifica la fecha inicial del periodo que se quiere consultar")
    afecha = serializers.DateField(format="%Y-%m-%d", required=False,help_text="se especifica la fecha final del periodo que se quiere consultar")
    limite = serializers.IntegerField(required=False,help_text="Estabele un numero de movimientos a mostrar")
    movimiento=serializers.CharField(required=False, help_text="Establece un tipo de movimiento que se quiere filtrar")
    estatus=serializers.CharField(required=False,help_text="Establece el estatus de los movimientos que se quieren filtrar")

    def validate(self, data):
        defecha = data.get("defecha")
        afecha = data.get("afecha")

        if defecha and afecha and defecha > afecha:
            raise serializers.ValidationError("defecha no puede ser mayor que afecha")

        return data
