from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters

from drf_yasg.utils import swagger_auto_schema

from tag.models import Tag

from main.serializers import NameSerializer, NoneSerializer


class TweetTagFilter(filters.FilterSet):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class TweetTagViewSet(ReadOnlyModelViewSet):
    serializer_class = NameSerializer
    filter_class = TweetTagFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def get_queryset(self):
        return Tag.objects.filter(tweets=self.kwargs['tweet_pk'])

    @swagger_auto_schema(method='get', responses={200: NoneSerializer})
    @action(detail=False, methods=['get'], url_path="count")
    def count(self, request, tweet_pk=None):
        res = self.get_queryset().aggregate(Count('id'))
        return Response({"count": res["id__count"]}, status=200)
