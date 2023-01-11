"""serializers for customer persona ficisa API"""
# Librerias Estandar
from datetime import timedelta, datetime

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_customers as exceptions
from .customers_serializers import DomicilioSerializer

CHOICES = [("value1", "México")]
CHOICES_2 = [("value1", "Mexicana")]


def validate_fields(attrs):
    """fuction to valiate fields"""
    # validattion for rfc leng of 13 caracters
    rfc_validate = attrs.get("rfc")
    if not str(rfc_validate).isalnum() and len(str(rfc_validate)) != 13:
        raise exceptions.InvalidRFC

    # validate for the user is adult
    try:
        fecha_nacimiento = attrs.get("fecha_nacimiento")
    except ValueError:
        raise serializers.ValidationError("Formato de fecha invalida fecha_nacimiento")
    now = datetime.now().date()
    adult_age = timedelta(days=365 * 18)
    if fecha_nacimiento >= now - adult_age:
        raise exceptions.InvalidYearOfBirth

    # validate curp leng  of 18 caracters
    curp_validate = attrs.get("curp")
    if not str(curp_validate).isalnum() and len(str(curp_validate)) != 18:
        raise exceptions.InvalidCurp


class DatosPersonalesSerializer(serializers.Serializer):
    """Serializer for datos personales field"""

    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()
    fecha_nacimiento = serializers.DateField()
    # pais_nacionalidad = serializers.ChoiceField(choices=CHOICES)
    # nacionalidad = serializers.ChoiceField(choices=CHOICES_2)
    pais_nacionalidad = serializers.CharField()
    nacionalidad = serializers.CharField()
    entidad_de_nacimiento = serializers.CharField()
    genero = serializers.CharField()
    telefono = serializers.IntegerField()
    rfc = serializers.CharField()
    regimen_fiscal = serializers.CharField()
    curp = serializers.CharField()
    cp_fiscal = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        validate_fields(attrs)
        return attrs


class PropietarioLegalSerializer(serializers.Serializer):
    """Serializer for datos del propietario real in case the user is no the owner"""

    curp = serializers.CharField()
    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()
    fecha_nacimiento = serializers.DateField()
    # pais_nacionalidad = serializers.ChoiceField(choices=CHOICES)
    # nacionalidad = serializers.ChoiceField(choices=CHOICES_2)
    pais_nacionalidad = serializers.CharField()
    nacionalidad = serializers.CharField()
    entidad_de_nacimiento = serializers.CharField()
    genero = serializers.CharField()
    # actividad
    ocupacion = serializers.CharField()
    rfc = serializers.CharField()
    regimen_fiscal = serializers.CharField()
    cp_fiscal = serializers.CharField()
    # domicilio
    domicilio = DomicilioSerializer()
    # contacto
    telefono = serializers.IntegerField()
    email = serializers.EmailField()

    def validate(self, attrs):
        validate_fields(attrs)
        return attrs


class PerfilTransaccionalPersonaFisicaSerializer(serializers.Serializer):
    """Serializer for perfil transaccional field"""

    ocupacion = serializers.CharField()
    giro = serializers.CharField()
    actividad = serializers.CharField()
    ingreso_mensual_neto = serializers.IntegerField()
    fuente_de_ingreso = serializers.CharField()
    procedencia_del_recuerso = serializers.CharField()
    ingresos_al_mes = serializers.IntegerField()
    operaciones_por_mes = serializers.IntegerField()
    destinatarios_operaciones = serializers.CharField()
    proveedores = serializers.CharField()
    cuenta_propia = serializers.BooleanField()


class OpenfinFisicaSerializer(serializers.Serializer):
    """Serializer for Open Fin Info"""

    datos_personales = DatosPersonalesSerializer()
    domicilio = DomicilioSerializer()
    perfil_transaccional = PerfilTransaccionalPersonaFisicaSerializer()
    propietario_legal = PropietarioLegalSerializer(required=False)


class CustomerPersonaFisicaSerializer(serializers.Serializer):
    """Serializer for Customers Persona Fisica"""

    id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    openfin_info = OpenfinFisicaSerializer(required=False)

    def to_representation(self, data):
        representation = super().to_representation(data.values())
        perfil_transaccional = representation.get("openfin_info", {}).get(
            "perfil_transaccional", {}
        )
        cuenta_propia = perfil_transaccional.get("cuenta_propia", False)

        if cuenta_propia:
            representation["openfin_info"].pop("propietario_legal", None)

        return representation


class CustomerQueryParamsSerializer(serializers.Serializer):
    """Serializer for Customer Query Params"""

    user_id = serializers.IntegerField(required=False)


class OpenFinPersonaFisicaSerializer(serializers.Serializer):
    """Serializer for Customers Persona Fisica"""

    id = serializers.IntegerField(required=False)
    informacion_general = OpenfinFisicaSerializer(required=False)

    def to_representation(self, data):
        representation = super().to_representation(data.values())
        perfil_transaccional = representation.get("informacion_general", {}).get(
            "perfil_transaccional", {}
        )
        cuenta_propia = perfil_transaccional.get("cuenta_propia", False)

        if cuenta_propia:
            representation["informacion_general"].pop("propietario_legal", None)

        return representation


class OpenFinPersonaFisicaQueryParamsSerializer(serializers.Serializer):
    """Serializer for Open Fin Customer Query Params"""

    user_id = serializers.IntegerField(required=False)
