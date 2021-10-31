from rest_framework import serializers


class DigitSerializer(serializers.Serializer):
    digit = serializers.CharField()
