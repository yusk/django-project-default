from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class StatusView(GenericAPIView):
    permission_classes = ()

    def get(self, request):
        return Response({"status": "ok"})
