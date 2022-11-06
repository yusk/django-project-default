from rest_framework import serializers


class JWTSerializer(serializers.Serializer):
    jwt = serializers.CharField()
