from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

from main.models import User
from main.helpers.jwt import gen_jwt
from main.serializers import (UserSerializer, UserPasswordSerializer,
                              TokenSerializer, UserDeleteSerializer)


class UserFilter(filters.FilterSet):
    def get_by_tweet_info(self, queryset, name, value):
        kwargs = {f"tweet__{name}": value}
        return queryset.filter(**kwargs).distinct()

    name__gt = filters.CharFilter(field_name='name', lookup_expr='gt')
    name__lt = filters.CharFilter(field_name='name', lookup_expr='lt')
    tweet = filters.CharFilter(method='get_by_tweet_info')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('name', 'name'),
    ), )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
        ]


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: UserSerializer}))
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.get_serializer(request.user,
                                         data=request.data,
                                         base64_required=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @method_decorator(decorator=swagger_auto_schema(
        responses={204: None}, request_body=UserDeleteSerializer))
    def delete(self, request):
        serializer = UserDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        if not user.check_password(serializer.validated_data["password"]):
            return Response({"password": "password not matched"})

        user.delete()
        return Response(None, 204)


class UserPasswordView(GenericAPIView):
    serializer_class = UserPasswordSerializer

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user

        if not user.check_password(serializer.validated_data["password"]):
            return Response({"password": "password not matched"})

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"token": gen_jwt(user)})


class UserViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_class = UserFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )
