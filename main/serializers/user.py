import os
import base64

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from main.models import User


class UserSerializer(serializers.ModelSerializer):
    icon_base64 = serializers.CharField(write_only=True)
    icon_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'icon_url', 'icon_base64', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True

    def update(self, instance, validated_data):
        if 'icon_base64' in validated_data:
            icon_base64 = validated_data.pop('icon_base64')
            tmp_path = os.path.join(
                settings.STATIC_ROOT,
                "%s.jpg" % timezone.now()
            )
            with open(tmp_path, 'wb') as f:
                f.write(base64.b64decode(icon_base64.encode()))
            with open(tmp_path, 'rb') as f:
                instance.icon.save(tmp_path, f)
        return super().update(instance, validated_data)

    def get_icon_url(self, obj):
        if obj.icon is None:
            return None
        try:
            return obj.icon.url
        except ValueError:
            return None
