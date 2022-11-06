from django.contrib import admin
from django.db.models import Model
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.safestring import mark_safe

from main import models
from main.models import User, Image
from main.utils import register_admin, get_field_names, get_many_to_many_names, export_as_json

admin.site.add_action(export_as_json, 'export_as_json')

# class TweetInline(admin.StackedInline):
#     model = Tweet
#     extra = 1
#     filter_horizontal = ('tags', )


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ['id', 'name', 'email']
    list_filter = ('is_staff', 'is_superuser')
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    filter_horizontal = get_many_to_many_names(User)

    actions = ['make_superuser']

    def get_list_display(self, request):
        list_display = get_field_names(User)
        list_display.append("image_show")
        return list_display

    @mark_safe
    def image_show(self, row):
        if row.icon:
            return f'<img src="{row.icon.url}" style="width:100px;height:auto;">'
        return ""

    @admin.action(description="選択された users をスーパーユーザーにする",
                  permissions=["change"])
    def make_superuser(self, request, queryset):
        num = queryset.update(is_superuser=True, is_staff=True)
        self.message_user(request, f"{num} 件の users をスーパーユーザーにしました。", level=20)
        return ""


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
