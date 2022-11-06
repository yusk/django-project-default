from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({"password": "パスワード確認がパスワードと一致していません。"})
        return attrs
