from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import logout_then_login

from . import views

app_name = 'main'
urlpatterns = []

if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    from rest_framework.routers import DefaultRouter, APIRootView
    from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

    router = DefaultRouter()
    router.APIRootView = APIRootView
    schema_view = get_swagger_view()

    urlpatterns.extend([
        path('', views.IndexView.as_view(), name='index'),
        path('api/', include(router.urls)),
        path('api/auth/dummy/', views.AuthDummyUserView.as_view()),
        path('api/auth/user/', obtain_jwt_token),
        path('api/auth/refresh/', refresh_jwt_token),
        path('api/auth/verify/', verify_jwt_token),
        path('api/user/', views.UserView.as_view()),
        path('signup/', views.SignupView.as_view(), name='signup'),
        path('signin/', views.SigninView.as_view(), name='signin'),
        path('signout/', logout_then_login, name='signout'),
        path('schema/', schema_view),
    ])
