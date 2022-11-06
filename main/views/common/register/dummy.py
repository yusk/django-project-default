from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from main.models import User
from main.serializers import NoneSerializer, TokenSerializer
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
