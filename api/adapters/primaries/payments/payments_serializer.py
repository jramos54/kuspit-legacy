"""Serializer for payments opening API"""
# Librerias Estandar
from datetime import datetime, date

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_dates as exceptions
from ....adapters.secondaries.Geolocation.geolocation_serializer import GeolocationSerializer



def validate_fields(attrs):
    """function to validate fields"""
    # Validation for payment date, can't be before the current date.
    payment_date = attrs.get("payment_date")
    payment_hour = attrs.get("payment_hour")

    if payment_date and payment_date < datetime.now().date():
        raise exceptions.InvalidDate

    if payment_hour:
        current_time = datetime.now().time()
        if payment_date == datetime.now().date() and payment_hour <= current_time:
            raise exceptions.InvalidHour

    # Search date validation
    start_date = attrs.get("defecha")
    end_date = attrs.get("afecha")

    # Check if start_date or end_date is None, set default values
    if start_date is None:
        start_date = date.min
    if end_date is None:
        end_date = date.max

    if start_date > end_date:
        raise exceptions.InvalidSearchDate


class PaymentSerializer(serializers.Serializer):
    """serializer for create payment"""

    kauxiliar = serializers.IntegerField(required=False)
    id_recipient = serializers.IntegerField(required=False)
    id_account = serializers.IntegerField(required=False)
    amount = serializers.FloatField(required=False)
    description = serializers.CharField(required=False)
    payment_date = serializers.DateField(required=False)
    reference = serializers.CharField(required=False)
    payment_hour = serializers.TimeField(required=False)

    def validate(self, attrs):
        validate_fields(attrs)
        return attrs


class PaymentGeolocationSerializer(serializers.Serializer):
    payment = PaymentSerializer(required=False)
    geolocalizacion = GeolocationSerializer(required=False)

    def to_representation(self, instance):
        """Personaliza la salida para mantener el JSON original"""
        data = super().to_representation(instance)

        # Fusiona geolocalización y datos de destinatario sin alterar el JSON original
        if data.get("geolocalizacion"):
            data.update(data.pop("geolocalizacion"))
        if data.get("payment"):
            data.update(data.pop("payment"))

        return data

    def to_internal_value(self, data):
        """Permite combinar los campos en la entrada sin requerir estructura anidada"""
        geolocation_data = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }

        # Usa el PaymentSerializer para validar los datos de payment
        payment_data = {
            "kauxiliar": data.get("kauxiliar"),
            "id_recipient": data.get("id_recipient"),
            "id_account": data.get("id_account"),
            "amount": data.get("amount"),
            "description": data.get("description"),
            "payment_date": data.get("payment_date"),
            "reference": data.get("reference"),
            "payment_hour": data.get("payment_hour"),
        }
        payment_serializer = PaymentSerializer(data=payment_data)
        payment_serializer.is_valid(raise_exception=True)
        payment = payment_serializer.validated_data

        internal_data = {
            "geolocalizacion": geolocation_data,
            "payment": payment
        }

        return super().to_internal_value(internal_data)


class OpenFinPaymentSerializer(serializers.Serializer):
    """serializer for get payment data from openfin api"""

    amount = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    row_id = serializers.IntegerField(required=False)
    row_info = serializers.CharField(required=False)
    payment_date = serializers.CharField(required=False, allow_null=True)
    pactivo = serializers.BooleanField(required=False, allow_null=True)
    wactivo = serializers.BooleanField(required=False)
    scheduled_time = serializers.CharField(required=False)
    alias = serializers.CharField(required=False)
    programed = serializers.BooleanField(required=False)
    creation_date = serializers.CharField(required=False)
    intension_date = serializers.CharField(required=False)
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    bank_institution = serializers.CharField(required=False, allow_null=True)
    num_account = serializers.IntegerField(required=False, allow_null=True)
    comision = serializers.FloatField(required=False, allow_null=True)
    IVA = serializers.FloatField(required=False, allow_null=True)
    total = serializers.FloatField(required=False, allow_null=True)
    RFC = serializers.CharField(required=False, allow_null=True)
    CURP = serializers.CharField(required=False, allow_null=True)


class PaymentQueryParamSerializer(serializers.Serializer):
    """Serializer for PaymentQueryParams"""

    id_transaction = serializers.IntegerField(required=False, allow_null=False)


class PaymentsQueryParamSerializer(serializers.Serializer):
    """Serializer for PaymentsQueryParams"""

    defecha = serializers.DateField(required=False, allow_null=False)
    afecha = serializers.DateField(required=False, allow_null=False)

    def validate(self, attrs):
        validate_fields(attrs)
        return attrs
