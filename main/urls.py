from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import logout_then_login

from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_nested.routers import NestedSimpleRouter

from . import views

router = DefaultRouter()
router.APIRootView = APIRootView
router.register('users', views.UserViewSet, basename='user')
router.register('tweets', views.TweetViewSet, basename='tweet')

tweet_router = NestedSimpleRouter(router, "tweets", lookup="tweet")
tweet_router.register('tags', views.DealViewSet, basename='tweet-tags')

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('api/', include(tweet_router.urls)),
    path('api/register/uuid/', views.RegisterUUIDView.as_view()),
    path('api/register/user/', views.RegisterUserView.as_view()),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),
    path('api/auth/uuid/', views.AuthUUIDView.as_view()),
    path('api/auth/user/', obtain_jwt_token),
    path('api/user/', views.UserView.as_view()),
    path('api/user/password/', views.UserPasswordView.as_view()),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', logout_then_login, name='signout'),
    path('profile/', views.UserDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.UserFormView.as_view(), name='profile_edit'),
]

if settings.DEBUG:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="API Schema",
            default_version='v1',
            description="",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    urlpatterns.extend([
        path('api/register/dummy/', views.RegisterDummyUserView.as_view()),
        path('schema/',
             schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
    ])
