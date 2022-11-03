import io
import base64

from rest_framework import serializers

from django.core.files.images import ImageFile
from django.db.models import ImageField


class MixInImageBase64Upload:
    def __init__(self, *args, **kwargs):
        base64_required = kwargs.pop("base64_required", True)
        self.image_field_names = []
        for f in self.Meta.model._meta.fields:
            if isinstance(f, ImageField):
                self.image_field_names.append(f.name)
                self.Meta.fields += (f.name, )
        super().__init__(*args, **kwargs)
        for name in self.image_field_names:
            self.fields[f"{name}_base64"] = serializers.CharField(
                write_only=True, required=base64_required)
            # self.fields[f"{name}_url"] = serializers.SerializerMethodField()
            # f = eval(f"lambda obj: getattr(getattr(obj, '{name}', None), 'url', None)")
            # setattr(self, f"get_{name}_url", f)
            self.fields[name].read_only = True

    def validate(self, data):
        for name in self.image_field_names:
            b64_name = f"{name}_base64"
            if b64_name in data:
                b = data.pop(b64_name)
                try:
                    data[name] = ImageFile(io.BytesIO(
                        base64.b64decode(b.encode())),
                                           name=f"{name}.png")
                except Exception:
                    raise serializers.ValidationError(
                        {name: "base64 decode error"})
        return data
