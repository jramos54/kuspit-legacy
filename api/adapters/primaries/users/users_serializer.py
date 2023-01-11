# Librerías de Terceros
from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    """Serializer for user location"""

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class UserLocationSerializer(serializers.Serializer):
    """Serializer for user location"""

    location = LocationSerializer()


class PermissionsSerializer(serializers.Serializer):
    """Serializer for permissions"""

    id = serializers.IntegerField(required=False)
    name = serializers.CharField()


class RoleSerializer(serializers.Serializer):
    """Serializer for roles"""

    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    permissions = PermissionsSerializer(many=True)


class BaseUserSerializer(serializers.Serializer):
    """Serializer for base user"""

    id = serializers.IntegerField(required=False)
    password = serializers.CharField(required=False)
    username = serializers.CharField()
    email = serializers.CharField()
    is_staff = serializers.BooleanField(required=False)
    is_customer = serializers.BooleanField(required=False)
    is_persona_fisica = serializers.BooleanField()
    is_persona_moral = serializers.BooleanField()


class AdministratorsSerializer(serializers.Serializer):
    """Serializer for users"""

    id = serializers.IntegerField(required=False)
    # name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()


class AdministratorsProfileSerializer(serializers.Serializer):
    """Serializer for users"""

    profile_info = AdministratorsSerializer()
    roles = RoleSerializer(many=True)


class NewUserSerializer(serializers.Serializer):
    """Serializer for base user"""

    password = serializers.CharField()
    nombre = serializers.CharField()
    paterno = serializers.CharField()
    materno = serializers.CharField()
    correo = serializers.CharField()
    persona_fisica = serializers.BooleanField()
