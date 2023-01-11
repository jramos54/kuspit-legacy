# Librerias Estandar
import re

# Librerías de Terceros
from rest_framework import serializers

# Proyecto

from ....engine.domain.exceptions import exceptions_recipient as exceptions

import re


class RecoveryPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    def validate(self, attrs):
        print("Entrando en el método validate")
        password = attrs.get('new_password')
        email = attrs.get('email')
        print(password)
        # Validación de la contraseña
        if len(password) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise serializers.ValidationError("La contraseña debe incluir caracteres alfanuméricos.")
        if email and email.split('@')[0] in password:
            raise serializers.ValidationError("La contraseña no puede contener el correo electrónico.")
        if re.search(r'(.)\1{3,}', password):
            raise serializers.ValidationError(
                "La contraseña no puede tener más de tres caracteres idénticos consecutivos.")
        if re.search(
                r'0123|1234|2345|3456|4567|5678|6789|7890|abcd|bcde|cdef|defg|efgh|fghi|ghij|hijk|ijkl|jklm|klmn|lmno|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz',
                password.lower()):
            raise serializers.ValidationError(
                "La contraseña no puede tener más de tres caracteres secuenciales numéricos o alfabéticos.")
        if 'dyp' in password.lower():
            raise serializers.ValidationError("La contraseña no puede contener la denominación comercial 'DyP'.")

        return attrs


class RecoveryTokenSerializer(serializers.Serializer):
    """Recipient Serializer"""
    # token = serializers.CharField(required=False)
    link = serializers.CharField(required=False)


class RecoveryQuestionsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    pregunta= serializers.CharField(max_length=250, required=False, allow_blank=True)
    respuesta=serializers.CharField(max_length=250, required=False, allow_blank=True)


class RecoveryTokenEmailSerializer(serializers.Serializer):
    """Recipient Serializer"""
    email = serializers.CharField(required=False)

