from rest_framework import serializers

from main.models import Image

from .base.image import MixInImageBase64Upload


class ImageSerializer(MixInImageBase64Upload, serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id',
            'created_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['created_at'].read_only = True
