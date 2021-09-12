from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema

from main.models import User
from main.serializers import NoneSerializer, TokenSerializer, UUIDSerializer, UserSignUpSerializer
from main.helpers import gen_jwt


class RegisterDummyUserView(GenericAPIView):
    serializer_class = NoneSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        user = User.objects.create_guest_user()
        user.name = 'dummy user'
        user.save()

        serializer = TokenSerializer(data={'token': gen_jwt(user)})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class RegisterUUIDView(GenericAPIView):
    serializer_class = UUIDSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(device_uuid=serializer.data['uuid']):
            message = {'detail': 'すでにそのユーザーは登録済みです。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_guest_user(
            device_uuid=serializer.data['uuid'])
        user.save()

        serializer = TokenSerializer(data={'token': gen_jwt(user)})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class RegisterUserView(GenericAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])
        user.save()

        serializer = TokenSerializer(data={'token': gen_jwt(user)})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
