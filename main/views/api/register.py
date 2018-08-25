from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.settings import api_settings

from main.models import User
from main.serializers import NoneSerializer, TokenSerializer

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
        serializer = TokenSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
