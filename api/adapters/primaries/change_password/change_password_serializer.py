from ....engine.domain.exceptions import exceptions_recipient as exceptions

import re
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        password_confirmation = attrs.get('password_confirmation')

        # Validación de que la nueva contraseña y su confirmación coincidan
        if new_password != password_confirmation:
            raise serializers.ValidationError("La confirmación de la contraseña no coincide con la nueva contraseña.")

        # Validación de longitud mínima
        if len(new_password) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        # Validación de caracteres alfanuméricos
        if not re.search(r'[A-Za-z]', new_password) or not re.search(r'[0-9]', new_password):
            raise serializers.ValidationError("La contraseña debe incluir caracteres alfanuméricos.")

        # Validación de caracteres idénticos consecutivos
        if re.search(r'(.)\1{3,}', new_password):
            raise serializers.ValidationError("La contraseña no puede tener más de tres caracteres idénticos consecutivos.")

        # Validación de caracteres secuenciales numéricos o alfabéticos
        if re.search(r'0123|1234|2345|3456|4567|5678|6789|7890|abcd|bcde|cdef|defg|efgh|fghi|ghij|hijk|ijkl|jklm|klmn|lmno|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz', new_password.lower()):
            raise serializers.ValidationError("La contraseña no puede tener más de tres caracteres secuenciales numéricos o alfabéticos.")

        # Validación de contenido restringido ('dyp')
        if 'dyp' in new_password.lower():
            raise serializers.ValidationError("La contraseña no puede contener la denominación comercial 'DyP'.")

        return attrs
