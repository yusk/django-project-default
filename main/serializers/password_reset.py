from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({"password": "password is need to be same to password_confirm."})
        return attrs
