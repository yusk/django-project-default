import traceback

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from main.models import AuthDigit, User, PasswordResetToken
from main.serializers import DigitSerializer, MessageSerializer, EmailSerializer, TokenSerializer, PasswordResetSerializer
from main.errors import TooManyEmailRequestError


class PasswordResetEmailView(GenericAPIView):
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
            auth.send_password_reset_email()
        except Exception:
            traceback.print_exc()
            auth.delete()
            message = {
                'message':
                'メールの送信に失敗しました。少しお待ちいただいてからもう一度送っていただくか、サービス運営者にお問合せください。'
            }
            return Response(message, status=500)

        serializer = MessageSerializer(
            data={
                'message':
                "メールアドレスにパスワードリセット用の確認コードを送信しました。コードを入力してパスワードの再設定を完了させてください。"
            })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PasswordResetDigitView(GenericAPIView):
    serializer_class = DigitSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
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

        prt = PasswordResetToken.update_or_create(auth.user)
        serializer = TokenSerializer(data={'token': prt.token})
        serializer.is_valid(raise_exception=True)
        auth.delete()
        return Response(serializer.data)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: MessageSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data["token"]

        prt = PasswordResetToken.objects.filter(token=token).last()
        if prt and prt.is_expired():
            serializer = MessageSerializer(
                data={'message': "パスワードリセットの有効期限が切れています。再度発行してください。"})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)
        elif prt is None or prt.token != token:
            serializer = MessageSerializer(
                data={'message': "パスワードリセットトークンが一致しませんでした。"})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=400)

        prt.user.set_password(serializer.data["password"])
        prt.user.save()
        prt.delete()

        serializer = MessageSerializer(data={'message': "パスワードの変更が完了しました。"})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
