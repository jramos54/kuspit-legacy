"""Serializer for account opening API"""
# Librerías de Terceros
from rest_framework import serializers


class AccountsSerializer(serializers.Serializer):
    """serializer for create account"""

    alias = serializers.CharField(required=False)
    type_account = serializers.IntegerField(required=False)


class OpenFinAccountsSerializer(serializers.Serializer):
    """serializer for get accounts from openfin api"""

    alias = serializers.CharField(required=False)
    clabe = serializers.CharField(required=False, allow_null=True)
    activo = serializers.BooleanField(required=False)
    saldo = serializers.FloatField(required=False)
    kauxiliar = serializers.IntegerField(required=False)


class AccountsQueryParamSerializer(serializers.Serializer):
    """serializer for filter accounts"""

    kauxiliar = serializers.IntegerField(required=False)
