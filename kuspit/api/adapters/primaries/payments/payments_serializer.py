from rest_framework import serializers


class PaymentsCustomersSerializer(serializers.Serializer):
    """Serializer for PaymentsCustomers"""

    id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    product_name = serializers.CharField()
    amount = serializers.FloatField()
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CustomerQueryParamsSerializer(serializers.Serializer):
    """Serializer for CustomerQueryParams"""

    customer_id = serializers.IntegerField(required=False)
