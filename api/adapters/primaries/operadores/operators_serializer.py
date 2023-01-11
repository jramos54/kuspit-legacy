# Librerías de Terceros
from rest_framework import serializers

from apps.backoffice.models.roles_model import RolesGroups


class PermissionsOperatorSerializer(serializers.Serializer):
    perfil = serializers.ChoiceField(choices=[
        ('dypfe_admin', 'Administrador DYPFE'),
        ('dypfe_analista', 'Analista DYPFE'),
        ('dypfe_autorizador', 'Tesorero DYPFE'),
        ('dypfe_user', 'Capturista DYPFE'),
        ('Sin_Perfil', 'Operador sin Perfil'),
        ('Sin_Acceso', 'Operador sin Acceso'),
        ('dypfe_tesorero', 'Tesorero DYPFE'),

    ])
    descripcion = serializers.CharField()

class OperatorSerializer(serializers.Serializer):
    """Operator Serializer"""
    idoperador = serializers.IntegerField()
    kasociado = serializers.IntegerField()
    nombre = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    ingreso = serializers.CharField(required=False, allow_blank=True)
    acceso = serializers.BooleanField(required=False)
    permisos = PermissionsOperatorSerializer(required=False)


class OperatorQueryParamSerializer(serializers.Serializer):
    idoperador = serializers.IntegerField(required=False, help_text="ID del operador al que se le asignará o quitará el rol.")
    perfil = serializers.ChoiceField(choices=[
        ('dypfe_admin', 'Administrador DYPFE'),
        ('dypfe_analista', 'Analista DYPFE'),
        ('dypfe_autorizador', 'Tesorero DYPFE'),
        ('dypfe_user', 'Capturista DYPFE'),
        ('dypfe_tesorero', 'Tesorero DYPFE'),

    ], required=False, help_text="Perfil que se asignará o quitará al operador.")
    tipo_acceso = serializers.ChoiceField(choices=[
        ('quitar', 'Quitar'),
        ('asignar', 'Asignar')
    ], required=False, help_text="Tipo de acción a realizar: 'quitar' para revocar el rol, 'asignar' para asignarlo.")


class NuevoOperadorSerializer(serializers.Serializer):
    """Recipient"""
    nombre = serializers.CharField(max_length=50, required=False, allow_blank=True)
    paterno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    materno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    correo = serializers.CharField(required=False, allow_blank=True)
    pfisica = serializers.BooleanField(required=False)


class RolesGroupsSerializer(serializers.ModelSerializer):
    rol_name=serializers.CharField(source='group.name', read_only=True)
    class Meta:
        model=RolesGroups
        fields=['rol_name']


