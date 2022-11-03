from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class TokenWithMessageSerializer(serializers.Serializer):
    token = serializers.CharField()
    message = serializers.CharField()
