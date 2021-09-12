from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters

from drf_yasg.utils import swagger_auto_schema

from main.models import Tag
from main.serializers import NameSerializer, NoneSerializer


class DealFilter(filters.FilterSet):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class DealViewSet(ReadOnlyModelViewSet):
    serializer_class = NameSerializer
    queryset = Tag.objects.all()
    filter_class = DealFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    @swagger_auto_schema(method='get', responses={200: NoneSerializer})
    @action(detail=False, methods=['get'], url_path="count")
    def count(self, request, tweet_pk=None):
        res = self.get_queryset().aggregate(Count('id'))
        return Response({"count": res["id__count"]}, status=200)
