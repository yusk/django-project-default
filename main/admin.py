from django.contrib import admin
from django.db.models import Model
from django.contrib.admin.sites import AlreadyRegistered

from main import models
from main.models import User, Tweet
from main.utils import register_admin, get_field_names


class TweetInline(admin.StackedInline):
    model = Tweet
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = get_field_names(User)
    inlines = [TweetInline]
    search_fields = ['id', 'name', 'email']


admin.site.register(User, UserAdmin)

# 残りのモデルを全て登録
for name in dir(models):
    obj = getattr(models, name)
    if not isinstance(obj, type):
        continue

    if issubclass(getattr(models, name), Model):
        try:
            register_admin(obj)
        except AlreadyRegistered:
            pass
