from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

from tag.models import Tag
from tweet.models import Tweet
from tweet.serializers import TweetSerializer

from main.serializers import NoneSerializer, NameSerializer

from main.utils import get_by_manytomany


class TweetFilter(filters.FilterSet):
    def get_by_manytomany0(self, queryset, name, value):
        return get_by_manytomany(queryset, name, value, 0)

    text_icontains = filters.CharFilter(field_name='text',
                                        lookup_expr='icontains')

    tag_name = filters.CharFilter(method='get_by_manytomany0')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('text', 'text'),
        ('created_at', 'created_at'),
    ), )

    class Meta:
        model = Tweet
        fields = [
            "id",
        ]


class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.prefetch_related("tags")
    filter_class = TweetFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        tweet = self.get_object()
        tweet.status = 0
        tweet.save()
        return Response(self.get_serializer(tweet).data)

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def draft(self, request, pk=None):
        tweet = self.get_object()
        tweet.status = 1
        tweet.save()
        return Response(self.get_serializer(tweet).data)

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def private(self, request, pk=None):
        tweet = self.get_object()
        tweet.status = 2
        tweet.save()
        return Response(self.get_serializer(tweet).data)

    @swagger_auto_schema(request_body=NameSerializer)
    @action(detail=True, methods=['post'], url_path="tag/add")
    def add_tag(self, request, pk=None):
        tweet = self.get_object()
        serializer = NameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag, _ = Tag.objects.get_or_create(name=serializer.data["name"])
        tweet.tags.add(tag)
        return Response(self.get_serializer(tweet).data)

    @swagger_auto_schema(request_body=NameSerializer)
    @action(detail=True, methods=['post'], url_path="tag/remove")
    def remove_tag(self, request, pk=None):
        tweet = self.get_object()
        serializer = NameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag, _ = Tag.objects.get_or_create(name=serializer.data["name"])
        tweet.tags.remove(tag)
        return Response(self.get_serializer(tweet).data)
