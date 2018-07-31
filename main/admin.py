from django.contrib import admin

from main.models import User
from main.utils import get_field_names


class UserAdmin(admin.ModelAdmin):
    list_display = get_field_names(User)


admin.site.register(User, UserAdmin)
