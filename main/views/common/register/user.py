import traceback

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from main.models import User, AuthDigit
from main.serializers import TokenSerializer, UserSignUpSerializer, MessageSerializer
from main.helpers import gen_jwt
from main.errors import TooManyEmailRequestError


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


class RegisterUserViewWithEmail(GenericAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: MessageSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = dict(serializer.validated_data)
        validated_data.pop("password_confirm")

        user = User.objects.create_user(**validated_data)

        try:
            auth = AuthDigit.update_or_create(user)
            auth.send_confirm_email()
        except TooManyEmailRequestError as e:
            user.delete()
            serializer = MessageSerializer(data={'message': e.message})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)
        except Exception:
            traceback.print_exc()
            user.delete()
            message = {
                'message':
                'メールの送信に失敗しました。少しお待ちいただいてからもう一度送っていただくか、サービス運営者にお問合せください。'
            }
            return Response(message, status=500)

        serializer = MessageSerializer(
            data={
                'message': "登録いただいたメールアドレスに確認コードを送信しました。コードを入力して登録を完了させてください。"
            })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
