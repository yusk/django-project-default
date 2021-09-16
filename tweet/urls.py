from django.urls import path, include

from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework_nested.routers import NestedSimpleRouter

from . import views

router = DefaultRouter()
router.APIRootView = APIRootView
router.register('tweets', views.TweetViewSet, basename='tweet')

tweet_router = NestedSimpleRouter(router, "tweets", lookup="tweet")
tweet_router.register('tags', views.TweetTagViewSet, basename='tweet-tags')

app_name = 'tweet'
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(tweet_router.urls)),
]
