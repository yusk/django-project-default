from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import User

from .base import MixInImageBase64Upload


class UserSerializer(MixInImageBase64Upload, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'icon', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({"password": "password is need to be same to password_confirm."})
        if User.objects.filter(email=attrs["email"]).count() > 0:
            raise ValidationError({"email": "This email has been already registered."})
        return attrs


class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise ValidationError({"new_password": "new_password is need to be same to new_password_confirm."})
        if attrs["password"] == attrs["new_password"]:
            raise ValidationError({"new_password": "new_password is need to be different to password."})
        return attrs


class UserDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
