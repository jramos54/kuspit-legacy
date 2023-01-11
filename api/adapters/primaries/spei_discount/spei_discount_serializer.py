from rest_framework import serializers


class SpeiDicountSerializer(serializers.Serializer):
    kauxiliar = serializers.IntegerField(required=False)
    idcuentab = serializers.IntegerField(required=False)