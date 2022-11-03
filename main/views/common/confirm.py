import traceback

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from main.models import AuthDigit, User
from main.serializers import (DigitSerializer, MessageSerializer,
                              TokenWithMessageSerializer, EmailSerializer)
from main.errors import TooManyEmailRequestError


class ConfirmDigitView(GenericAPIView):
    serializer_class = DigitSerializer
    permission_classes = ()

    @method_decorator(decorator=swagger_auto_schema(responses={
        200: TokenWithMessageSerializer,
        400: MessageSerializer
    }))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data["digit"]

        auth = AuthDigit.objects.filter(code=code).last()
        if auth and auth.is_expired():
            serializer = MessageSerializer(
                data={'message': "確認コードの有効期限が切れています。再度発行してください。"})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)
        elif auth is None or auth.code != code:
            serializer = MessageSerializer(
                data={'message': "確認コードが一致しませんでした。"})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)

        auth.user.email_confirmed = True
        auth.user.save()
        auth.delete()

        token = auth.user.get_jwt()

        serializer = TokenWithMessageSerializer(data={
            'message': "確認コードが認証されました。",
            "token": token,
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ConfirmDigitResetView(GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: MessageSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]

        user = User.objects.filter(email=email).first()
        if user is None:
            serializer = MessageSerializer(
                data={'message': "登録されたユーザーが見つかりませんでした。"})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)

        try:
            auth = AuthDigit.update_or_create(user=user)
        except TooManyEmailRequestError as e:
            serializer = MessageSerializer(data={'message': e.message})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)
        try:
            auth.send_confirm_email()
        except Exception:
            traceback.print_exc()
            auth.delete()
            message = {
                'message':
                'メールの送信に失敗しました。少しお待ちいただいてからもう一度送っていただくか、サービス運営者にお問合せください。'
            }
            return Response(message, status=500)

        serializer = MessageSerializer(
            data={'message': "メールアドレスに確認コードを再送信しました。コードを入力して登録を完了させてください。"})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
