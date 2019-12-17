from django.contrib import admin
from django.db.models import Model
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.safestring import mark_safe

from main import models
from main.models import User, Tweet
from main.utils import register_admin, get_field_names, export_as_json

admin.site.add_action(export_as_json, 'export_as_json')


class TweetInline(admin.StackedInline):
    model = Tweet
    extra = 1
    filter_horizontal = ('tags', )


class UserAdmin(admin.ModelAdmin):
    inlines = [TweetInline]
    search_fields = ['id', 'name', 'email']
    list_filter = ('is_staff', 'is_superuser')
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def get_list_display(self, request):
        list_display = get_field_names(User)
        list_display.append("image_show")
        return list_display

    @mark_safe
    def image_show(self, row):
        if row.icon:
            return f'<img src="{row.icon.url}" style="width:100px;height:auto;">'
        return ""


class TweetAdmin(admin.ModelAdmin):
    list_display = get_field_names(Tweet)
    list_editable = ['status']
    list_filter = ('status', )
    list_per_page = 100
    list_select_related = ('user', )
    search_fields = ['text']
    filter_horizontal = ('tags', )
    ordering = None
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    actions = ['make_unpublished']

    def make_unpublished(self, request, queryset):
        rows_updated = queryset.update(status=2)

        if rows_updated == 1:
            message_bit = "1 tweet was"
        else:
            message_bit = f"{rows_updated} tweets were"

        self.message_user(
            request, f"{message_bit} successfully marked as unpublished.")

    make_unpublished.short_description = "選択された tweets を非公開に"
    make_unpublished.allowed_permissions = ('change', )

    def view_tags(self, obj):
        return ",".join([tag.name for tag in obj.get_all_tags()])

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display.extend(["view_tags", "get_tag_count", "get_tag_added_at"])
        return list_display


admin.site.register(User, UserAdmin)
admin.site.register(Tweet, TweetAdmin)

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
