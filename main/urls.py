from django.urls import path, include
from django.conf import settings

from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

router = DefaultRouter()
router.APIRootView = APIRootView
router.register('users', views.UserViewSet, basename='user')
router.register('images', views.ImageViewSet, basename='image')

app_name = 'main'
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/status/', views.StatusView.as_view()),
    path('api/register/uuid/', views.RegisterUUIDView.as_view()),
    path('api/register/user/', views.RegisterUserView.as_view()),
    # path('api/register/user/', views.RegisterUserViewWithEmail.as_view()),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),
    path('api/auth/uuid/', views.AuthUUIDView.as_view()),
    path('api/auth/user/', obtain_jwt_token),
    # path('api/auth/user/', views.AuthUserViewWithEmail.as_view()),
    # path('api/confirm/digit/', views.ConfirmDigitView.as_view()),
    # path('api/confirm/digit/reset/', views.ConfirmDigitResetView.as_view()),
    # path('api/password/', views.PasswordResetView.as_view()),
    # path('api/password/email/', views.PasswordResetEmailView.as_view()),
    # path('api/password/digit/', views.PasswordResetDigitView.as_view()),
    path('api/user/', views.UserView.as_view()),
    path('api/user/password/', views.UserPasswordView.as_view()),
]

if settings.DEBUG:
    permission_classes = [permissions.AllowAny]
    urlpatterns.extend([
        path('api/register/dummy/', views.RegisterDummyUserView.as_view()),
    ])
else:
    permission_classes = [permissions.IsAdminUser]

schema_view = get_schema_view(
    openapi.Info(
        title="API Schema",
        default_version='v1',
        description="",
    ),
    public=True,
    permission_classes=permission_classes,
)

urlpatterns.extend([
    path('schema/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
])
