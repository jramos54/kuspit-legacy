# Librerias Estandar
import re

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_recipient as exceptions
from ....adapters.secondaries.Geolocation.geolocation_serializer import GeolocationSerializer


class PaymentFilesImportedSerializer(serializers.Serializer):
    # Define los campos esperados en el archivo
    _id = serializers.IntegerField(required=False)
    Archivo= serializers.CharField(required=False)
    Aplicado=serializers.BooleanField(required=False)


class PaymentDetailImportedSerielizer(serializers.Serializer):
    idarchivo = serializers.IntegerField(allow_null=True)
    idpago = serializers.IntegerField(allow_null=True)
    institucion_contraparte = serializers.CharField(allow_null=True, max_length=255)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    nombre_beneficiario = serializers.CharField(allow_null=True, max_length=255)
    tipo_cuenta_beneficiario = serializers.CharField(allow_null=True, max_length=255)
    cuenta_beneficiario = serializers.CharField(allow_null=True, max_length=255)
    concepto_pago = serializers.CharField(allow_null=True, max_length=255)
    referencia_numerica = serializers.CharField(allow_null=True, max_length=255)
    idtransaccion = serializers.IntegerField(allow_null=True, required=False)
    comision = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
    fecha_real = serializers.DateTimeField(allow_null=True, required=False)
    msg = serializers.CharField(allow_null=True, required=False)


class QueryIdSerializer(serializers.Serializer):
    idarchivo = serializers.IntegerField(required=False)
    kauxiliar = serializers.IntegerField(required=False)


class PaymentFileUpload(serializers.Serializer):
    file = serializers.FileField(allow_empty_file=False, required=True)
    kauxiliar = serializers.IntegerField(required=True)

    def validate_file(self, value):
        # Verificar si el archivo es un CSV
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("El archivo debe estar en formato CSV.")
        return value


class PaymentFileUploadGeolocation(serializers.Serializer):
    file_upload = PaymentFileUpload(required=False)
    geolocalizacion = GeolocationSerializer(required=False)

    def to_representation(self, instance):
        """Personaliza la salida para mantener el JSON original"""
        data = super().to_representation(instance)

        # Fusiona geolocalización y datos de archivo sin alterar el JSON original
        if data.get("geolocalizacion"):
            data.update(data.pop("geolocalizacion"))
        if data.get("file_upload"):
            data.update(data.pop("file_upload"))

        return data

    def to_internal_value(self, data):
        """Permite combinar los campos en la entrada sin requerir estructura anidada"""
        # Extraer los datos de geolocalización de la entrada
        geolocation_data = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }

        # Extraer los datos de carga de archivo de la entrada
        file_upload_data = {
            "file": data.get("file"),
            "kauxiliar": data.get("kauxiliar"),
        }

        internal_data = {
            "geolocalizacion": geolocation_data,
            "file_upload": file_upload_data,
        }

        return super().to_internal_value(internal_data)
