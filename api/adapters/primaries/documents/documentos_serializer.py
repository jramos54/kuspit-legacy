"""Serializers for File Upload Service"""
# Librerías de Terceros
from rest_framework import serializers


class DataDocumentSerializer(serializers.Serializer):
    """serializer for files"""

    file_1 = serializers.FileField(required=False)


class DocumentSerializer(serializers.Serializer):
    """serializer for files"""

    uuid = serializers.CharField(required=False)
    b64 = serializers.CharField(required=False)


class DocumentsQuerySerializer(serializers.Serializer):
    """serializer for filter documents"""

    openfin_id = serializers.IntegerField(required=False)
    type_id = serializers.IntegerField(required=False)


# =================== OPEN FIN ===================


class OpenFinCatDocumentsSerializer(serializers.Serializer):
    """serializer for object that contains document structure"""

    idtipo = serializers.IntegerField(required=False)
    nombre = serializers.CharField(required=False)


class OpenFinDocumentsSerializer(serializers.Serializer):
    """serializer for object that contains document structure"""

    # id = serializers.IntegerField(required=False)   # id del usuario en open fin
    idtipo = serializers.IntegerField(required=False)
    b64 = serializers.CharField(required=False)
