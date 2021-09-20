from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import logout_then_login

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', logout_then_login, name='signout'),
    path('profile/', views.UserDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.UserFormView.as_view(), name='profile_edit'),
]
