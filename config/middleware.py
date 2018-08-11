import traceback

from django.utils.deprecation import MiddlewareMixin


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
