import os
import uuid

from django.db import models
from django.utils import timezone


def image_file_path(instance, filename):
    return "img/%s%s" % (timezone.now(), os.path.splitext(filename)[1])


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
