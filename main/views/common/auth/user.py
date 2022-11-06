from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from ipware import get_client_ip

from main.models import LoginInvalid

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthUserViewWithEmail(ObtainJSONWebToken):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        client_addr, _ = get_client_ip(request)
        message = LoginInvalid.invalid(client_addr)
        if message:
            message = {'message': message}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.object.get('user') or request.user
            if not user.email_confirmed:
                message = {'message': '先にメール確認を完了させてください。'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            codes = []
            for v in e.get_codes().values():
                codes.extend(v)
            codes = set(codes)
            if "invalid" in codes:
                LoginInvalid.inc(client_addr)
            raise e

        return super().post(request, *args, **kwargs)
