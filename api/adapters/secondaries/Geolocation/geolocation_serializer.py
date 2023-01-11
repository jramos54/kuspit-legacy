from rest_framework import serializers


class GeolocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=18, decimal_places=15, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=18, decimal_places=15, required=False, allow_null=True)
    ip = serializers.IPAddressField(required=False, allow_null=True)
