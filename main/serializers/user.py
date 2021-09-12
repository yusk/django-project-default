from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import User


class UserSerializer(serializers.ModelSerializer):
    icon_base64 = serializers.CharField(write_only=True, required=False)
    icon_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'icon_url', 'icon_base64', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['id'].read_only = True

    def update(self, instance, validated_data):
        if 'icon_base64' in validated_data:
            icon_base64 = validated_data.pop('icon_base64')
            instance.save_icon_with_base64(icon_base64)
        return super().update(instance, validated_data)

    def get_icon_url(self, obj):
        if obj.icon is None:
            return None
        try:
            return obj.icon.url
        except ValueError:
            return None


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
