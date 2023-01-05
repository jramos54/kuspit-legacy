from rest_framework import serializers


class NotFoundSerializer(serializers.Serializer):
    """Serializer for swagger documentation"""
    detail = serializers.CharField(help_text="El mensaje de error")