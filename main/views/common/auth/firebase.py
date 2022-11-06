from firebase_admin import auth

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from main.models import User
from main.serializers import TokenSerializer, JWTSerializer
from main.helpers import gen_jwt


class RegisterFirebaseView(GenericAPIView):
    serializer_class = JWTSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        jwt = serializer.validated_data["jwt"]
        decoded = auth.verify_id_token(jwt)
        uid = decoded["uid"]
        phone_number = decoded["phone_number"]
        email = f"{uid}@firebase.google.com"
        if User.objects.filter(email=email).first() is not None:
            return Response({"message": "既に登録されているユーザーです"}, status=400)
        user = User.objects.create_user(email=email,
                                        password=None,
                                        phone_number=phone_number)

        serializer = TokenSerializer(data={'token': gen_jwt(user)})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
