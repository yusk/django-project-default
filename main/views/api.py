from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.schemas import ManualSchema
from rest_framework.decorators import schema
from rest_framework_jwt.settings import api_settings

from main.models import User
from main.serializers import NoneSerializer, TokenOutputSerializer, UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterDummyUserView(GenericAPIView):
    serializer_class = NoneSerializer
    permission_classes = ()

    def post(self, request):
        user = User.objects.create_guest_user()
        user.name = 'dummy user'
        user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = TokenOutputSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    @schema(ManualSchema(fields=[]))
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
