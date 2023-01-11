# Librerías de Terceros
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_customers as exceptions
from .customers_serializers import OtrosDatosPersonalesSerializer, DomicilioSerializer


class DatosEmpresaSerializer(serializers.Serializer):
    razon_social = serializers.CharField()
    nacionalidad = serializers.CharField()
    rfc = serializers.CharField()
    num_ser_fir_elec = (
        serializers.IntegerField()
    )  # CONFIRMAR SI ES CAMPO COMPLETAMENTE NUMERICO
    giro_mercantil = serializers.CharField()

    # aqui deberia ir el serializador de la cuenta clabe
    cuenta_clabe = serializers.IntegerField()
    banco_cuenta_clabe = serializers.CharField()

    def validate(self, attrs):
        # validar la cuenta clabe si hay banco precargado
        cuenta_clabe_validate = attrs.get("cuenta_clabe")
        banco__cuenta_clabe_validate = attrs.get("banco_cuenta_clabe")

        if banco__cuenta_clabe_validate is None:
            raise exceptions.NotBank

        if len(str(cuenta_clabe_validate)) != 18:
            raise exceptions.InvalidClabeAccount
        return attrs


class DatosEscrituraConstitutivaSerielizer(serializers.Serializer):
    default_error_messages = {
        "invalid_rfc": _(exceptions.InvalidRFC.message),
    }

    fecha_constitucion = serializers.DateField(format="%Y-%m-%d")
    num_escritura = (
        serializers.IntegerField()
    )  # CONFIRMAR QUE SEA DATO COMPLETAMENTE NUMERICO
    fecha_protocolizacion = serializers.DateField(format="%Y-%m-%d")
    rfc = serializers.CharField()
    curp = serializers.CharField()

    def validate(self, attrs):
        # Validacion del RFC 12 caracteres alfanumericos
        rfc_validate = attrs.get("rfc")

        if not str(rfc_validate).isalnum() and len(str(rfc_validate)) != 12:
            raise exceptions.InvalidRFC
        # Validacion de CURP a 16 caracteres alfanumericos
        curp_validate = attrs.get("curp")

        if not str(curp_validate).isalnum() and len(str(curp_validate)) != 16:
            raise exceptions.InvalidCurp
        return attrs


class DatosRepresentanteLegalSerielizer(serializers.Serializer):
    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()
    email = serializers.EmailField()
    num_escr_pub = (
        serializers.IntegerField()
    )  # confirmar si este dato es completamente numerocio
    fecha_protocolizacion = serializers.DateField(format="%Y-%m-%d")
    firma_autografa = serializers.CharField()
    clave_lada = serializers.IntegerField()
    telefono = serializers.IntegerField()
    extencion = serializers.IntegerField()
    # Se agrega el serializador de CURP
    curp = serializers.CharField()
    rfc = serializers.CharField()

    def validate(self, attrs):
        # Validacion numero de telefono a 10 digitos
        num_tel_validate = attrs.get("telefono")

        if len(str(num_tel_validate)) != 10:
            raise exceptions.InvalidPhoneNumber

        # Validacion de CURP a 16 caracteres alfanumericos
        curp_validate = attrs.get("curp")

        if not str(curp_validate).isalnum() and len(str(curp_validate)) != 16:
            raise exceptions.InvalidCurp

        rfc_validate = attrs.get("rfc")

        if not str(rfc_validate).isalnum() and len(str(rfc_validate)) != 13:
            raise exceptions.InvalidRFC
        return attrs


class DatosDeContactoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    telefono = serializers.IntegerField()
    razon_social = serializers.CharField()
    rfc = serializers.CharField()
    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()

    def validate(self, attrs):
        # Validacion numero de telefono a 10 digitos
        num_tel_validate = attrs.get("telefono")

        if len(str(num_tel_validate)) != 10:
            raise exceptions.InvalidPhoneNumber

        # Validacion del RFC 12 caracteres alfanumericos
        rfc_validate = attrs.get("rfc")

        if not str(rfc_validate).isalnum() and len(str(rfc_validate)) != 13:
            raise exceptions.InvalidRFC
        return attrs


class PerfilTransaccionalSerializer(serializers.Serializer):
    """Serializer for transactional profile"""

    ocupacion = serializers.CharField()
    giro = serializers.CharField()
    actividad_economica = serializers.CharField()
    ingreso_mensual = serializers.FloatField()
    fuente_ingresos = serializers.CharField()
    procedencia_recurso = serializers.CharField()
    estimado_mensual = serializers.FloatField()
    operaciones_mensual = serializers.IntegerField()
    destino_transferencia = serializers.CharField()  # puede cambiar a opciones
    utilizacion_recursos = serializers.CharField()
    actuas_cuenta_propia = serializers.BooleanField(default=True)
    nombre_comercial = serializers.CharField()


class DatosPropietarioRealSerializer(serializers.Serializer):
    """datos de propietario real"""

    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()
    fecha_nacimiento = serializers.DateField(format="%Y-%m-%d")
    pais_nacimiento = serializers.CharField()
    estado = serializers.CharField()
    genero = serializers.CharField()
    nacionalidad = serializers.CharField()
    curp = serializers.CharField()
    ocupacion = serializers.CharField()
    giro = serializers.CharField()
    actividad = serializers.CharField()
    rfc = serializers.CharField()
    firma_electronica = serializers.CharField()
    calle = serializers.CharField()
    num_exterior = serializers.CharField()
    num_interior = serializers.CharField()
    cp = serializers.IntegerField()
    municipio = serializers.CharField()
    colonia = serializers.CharField()
    estado = serializers.CharField()
    pais = serializers.CharField()
    celular = serializers.IntegerField()
    correo = serializers.EmailField()

    def validate(self, attrs):
        # Validacion numero de telefono a 10 digitos
        num_tel_validate = attrs.get("celular")

        if len(str(num_tel_validate)) != 10:
            raise exceptions.InvalidPhoneNumber

        # Validacion del RFC 12 caracteres alfanumericos
        rfc_validate = attrs.get("rfc")

        if not str(rfc_validate).isalnum() and len(str(rfc_validate)) != 13:
            raise exceptions.InvalidRFC

        # Validacion de CURP a 16 caracteres alfanumericos
        curp_validate = attrs.get("curp")

        if not str(curp_validate).isalnum() and len(str(curp_validate)) != 16:
            raise exceptions.InvalidCurp
        return attrs


class OpenfinMoralSerializer(serializers.Serializer):
    """serlializer for Open Fin Info"""

    # idsucursal = serializers.CharField()
    # idrol = serializers.CharField()
    # empresa = serializers.CharField()
    # domicilio = DomicilioSerializer()
    # telefono = serializers.IntegerField()
    # fecha_constitucion = serializers.DateField(format="%Y-%m-%d")
    # pais_nacionalidad = serializers.CharField()
    # rfc = serializers.CharField()
    # idgiro = serializers.CharField()
    ##apartir de aqui es conforme estan en las pantallas que raudys propociono
    datos_empresa = DatosEmpresaSerializer()
    escritura_constitutiva = DatosEscrituraConstitutivaSerielizer()
    representante_legal = DatosRepresentanteLegalSerielizer()
    domicilio = DomicilioSerializer()
    otros_datos_personales = OtrosDatosPersonalesSerializer()
    datos_de_contacto = DatosDeContactoSerializer()
    # perfil_transaccional = PerfilTransaccionalSerializer()
    # propietario_real = DatosPropietarioRealSerializer()


class CustomerPersonaMoralSerializer(serializers.Serializer):
    """Serializer for Persona Moral Serializer"""

    # id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    openfin_info = OpenfinMoralSerializer(required=False)


class CustomerQueryParamsSerializer(serializers.Serializer):
    """Serializer for Customer Query Params"""

    # id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    # openfin_info= OpenfinMoralSerializer(required=False)


class OpenFinPersonaMoralSerializer(serializers.Serializer):
    """Serializer for Open fin info of Customers Persona Fisica"""

    id = serializers.IntegerField(required=False)
    informacion_general = OpenfinMoralSerializer(required=False)


class OpenFinPersonaMoralQueryParamsSerializer(serializers.Serializer):
    """Serializer for open fin customer query params"""

    user_id = serializers.IntegerField(required=False)
    # openfin_info = OpenFinInfoSerializer(required=False)
