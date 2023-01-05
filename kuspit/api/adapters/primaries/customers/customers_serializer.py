from abc import ABC
from rest_framework import serializers


class CustomersSerializer(serializers.Serializer):
    """Serializer for Customers"""

    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    paternal_surname = serializers.CharField()
    email = serializers.CharField()

class CustomerQueryParamsSerializer(serializers.Serializer):
    """Serializer for CustomerQueryParams"""

    customer_id = serializers.IntegerField(required=False)
