from rest_framework import serializers

from main.models import User
from main.utils import get_field_names


class NoneSerializer(serializers.Serializer):
    pass


class TokenOutputSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = get_field_names(User)
