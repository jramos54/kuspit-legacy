"""views for frequent questions service"""

# Librerías de Terceros
from rest_framework import serializers


class FrequentQuestionsSerializer(serializers.Serializer):
    """class for frequent questions views without authentication"""

    id = serializers.IntegerField()
    question = serializers.CharField(required=False)
    answer = serializers.CharField(required=False)
    is_active = serializers.BooleanField()


class FrequentQuestionsQueryParamsSerializer(serializers.Serializer):
    """class for frequent questions views with authentication"""

    id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
