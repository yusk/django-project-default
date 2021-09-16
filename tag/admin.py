from django.db.models import Model
from django.contrib.admin.sites import AlreadyRegistered

from tag import models
from main.utils import register_admin

for name in dir(models):
    obj = getattr(models, name)
    if not isinstance(obj, type):
        continue

    if issubclass(getattr(models, name), Model):
        try:
            register_admin(obj)
        except AlreadyRegistered:
            pass
