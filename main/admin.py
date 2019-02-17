from django.contrib import admin
from django.db.models import Model

from main import models
from main.utils import register_admin

for name in dir(models):
    obj = getattr(models, name)
    if not isinstance(obj, type):
        continue

    if issubclass(getattr(models, name), Model):
        register_admin(obj)
