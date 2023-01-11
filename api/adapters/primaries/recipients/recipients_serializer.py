# Librerias Estandar
import re

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....adapters.secondaries.Geolocation.geolocation_serializer import GeolocationSerializer
from ....adapters.primaries.recipients_accounts import (
    recipients_accounts_serializer as account_serializer,
)
from ....engine.domain.exceptions import exceptions_recipient as exceptions


class RecipientSerializer(serializers.Serializer):
    """Recipient Serializer"""

    iddestinatario = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=50, required=False, allow_blank=True)
    paterno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    materno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rfc = serializers.CharField(required=False, allow_blank=True)
    curp = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    correo = serializers.CharField(required=False, allow_blank=True)
    pfisica = serializers.BooleanField(required=False)
    cuentas = serializers.ListSerializer(
        child=account_serializer.RecipientAccountSerializer(), required=False
    )


    def validate(self, attrs):
        """Validaciones"""
        if self.partial:
            return attrs

        rfc_validate = attrs.get("rfc")
        if rfc_validate != "":
            # Expresión regular para personas físicas y morales
            patron_rfc = (
                r"^"  # Inicio de la cadena
                r"[A-Z&Ñ]{3,4}"  # 3 o 4 letras o & y Ñ para el nombre o razón social
                r"\d{6}"  # 6 dígitos para la fecha (año, mes, día)
                r"[A-Z0-9]{3}"  # Tres últimos caracteres alfanuméricos
                r"$"  # Fin de la cadena
            )
            if not re.match(patron_rfc, rfc_validate):
                print(rfc_validate)
                raise exceptions.InvalidRFC

        # longitud CURP
        curp_validate = attrs.get("curp")
        if curp_validate != "":
            patron_curp = r"^[A-Z]{4}\d{6}[H,M][A-Z]{5}[A-Z0-9]{2}$"
            if curp_validate and not re.match(patron_curp, curp_validate):
                raise exceptions.InvalidCURP

        return attrs


class RecipientGeolocationSerializer(serializers.Serializer):
    geolocalizacion = GeolocationSerializer(required=False)
    recipient_data = RecipientSerializer(required=False)

    def to_representation(self, instance):
        """Personaliza la salida para mantener el JSON original"""
        data = super().to_representation(instance)

        # Fusiona geolocalización y datos de destinatario sin alterar el JSON original
        if data.get("geolocalizacion"):
            data.update(data.pop("geolocalizacion"))
        if data.get("recipient_data"):
            data.update(data.pop("recipient_data"))

        return data

    def to_internal_value(self, data):
        """Permite combinar los campos en la entrada sin requerir estructura anidada"""
        geolocation_data = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
        recipient_data = {
            key: value
            for key, value in {
                "iddestinatario": data.get("iddestinatario"),
                "nombre": data.get("nombre"),
                "paterno": data.get("paterno"),
                "materno": data.get("materno"),
                "rfc": data.get("rfc"),
                "curp": data.get("curp"),
                "is_active": data.get("is_active"),
                "correo": data.get("correo"),
                "pfisica": data.get("pfisica"),
            }.items()
            if value is not None
        }

        internal_data = {
            "geolocalizacion": geolocation_data,
            "recipient_data": recipient_data
        }

        return super().to_internal_value(internal_data)

class RecipientQueryParamSerializer(serializers.Serializer):
    iddestinatario = serializers.IntegerField(required=False)


class DestinatarioSerializer(serializers.Serializer):
    """Recipient"""

    nombre = serializers.CharField(max_length=50, required=False, allow_blank=True)
    paterno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    materno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rfc = serializers.CharField(required=False, allow_blank=True)
    curp = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    correo = serializers.CharField(required=False, allow_blank=True)
    pfisica = serializers.BooleanField(required=False)
