# Librerias Estandar
import re

# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_recipient as exceptions


class FilesImportedSerializer(serializers.Serializer):
    # Define los campos esperados en el archivo
    Id = serializers.IntegerField(required=False)
    Archivo= serializers.CharField(required=False)
    Fecha= serializers.CharField(required=False)
    Cargado_por= serializers.CharField(required=False)
    Aplicado=serializers.BooleanField(required=False)


class DetailImportedSerielizer(serializers.Serializer):
    idarchivo = serializers.IntegerField()
    idregistro = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    tipo_persona = serializers.ChoiceField(
        choices=[('FISICA', 'Física'), ('MORAL', 'Moral')])  # Ajusta según tus opciones
    rfc = serializers.CharField(max_length=13)
    alias = serializers.CharField(max_length=50)
    institucion = serializers.CharField(max_length=5)
    tipo_cuenta_beneficiario = serializers.CharField(max_length=10)
    cuenta_beneficiario = serializers.CharField(max_length=18)
    limite_operacion = serializers.DecimalField(max_digits=10, decimal_places=2)
    numero_operaciones = serializers.IntegerField()
    email = serializers.EmailField()
    fecha_real = serializers.CharField(max_length=255,allow_null=True)# serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S.%f %Z", input_formats=['%d/%m/%Y %H:%M:%S.%f %Z'])
    idbeneficiario = serializers.IntegerField(allow_null=True)
    msg = serializers.CharField(max_length=255,allow_null=True)

class QueryIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
