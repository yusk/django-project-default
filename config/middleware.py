import jwt
import traceback

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from main.models import User


class RequestHandleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_exception(self, request, exception):
        print(traceback.format_exc())

    def process_response(self, request, response):
        if response.status_code in [500]:
            message = '\n'.join([
                '【%s %s】' % (request.method, request.get_full_path()),
                'status_code: %s' % str(response.status_code)
            ])
            print(message)
        return response


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        auth_header = None
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode()
        else:
            pass

        if auth_header:
            auth_kind = None
            if len(auth_header.split(' ')) == 2:
                auth_kind, auth_value = auth_header.split(' ')
            if auth_kind == 'JWT':
                try:
                    user_jwt = jwt.decode(
                        auth_value,
                        settings.SECRET_KEY,
                    )
                    scope['user'] = User.objects.get(
                        id=user_jwt['user_id']
                    )
                except (KeyError, jwt.InvalidSignatureError, jwt.ExpiredSignatureError, jwt.DecodeError):
                    traceback.print_exc()
                except Exception:
                    traceback.print_exc()

        return self.inner(scope)
