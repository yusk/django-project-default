from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse

from .funcs import get_field_names


def create_admin(cls):
    return type("%sAdmin" % cls.__name__, (admin.ModelAdmin, ),
                {"list_display": get_field_names(cls)})


def register_admin(cls):
    admin.site.register(cls, create_admin(cls))


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


export_as_json.short_description = "選択された objects を json で出力"
export_as_json.allowed_permissions = ('view', )
