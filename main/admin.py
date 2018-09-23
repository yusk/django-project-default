from django.contrib import admin

from main.models import User
from main.utils import register_admin

for cls in [User]:
    register_admin(cls)
