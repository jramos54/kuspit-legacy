"""Serializer for products opening API"""
# Librerías de Terceros
from rest_framework import serializers


class ProductsSerialazer(serializers.Serializer):
    """serializer for datos of products"""

    idproducto = serializers.IntegerField(required=False)
    nombre = serializers.CharField(required=False)


class ProductsQueryParamSerialazer(serializers.Serializer):
    """serializer for filter products"""

    idproducto = serializers.IntegerField(required=False)
