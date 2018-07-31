from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = []

if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view()
    urlpatterns.extend([
        path('schema/', schema_view),
    ])
