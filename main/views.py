from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.settings import api_settings

from main.models import User
from main.forms import SignupForm, SigninForm
from main.serializers import NoneSerializer, TokenOutputSerializer, UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class IndexView(TemplateView):
    template_name = "main/index.html"


class SignupView(FormView):
    template_name = 'main/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.create_user()
        if user is None:
            return super().form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class SigninView(FormView):
    template_name = 'main/signin.html'
    form_class = SigninForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_authenticated_user()
        if user is None:
            return super().form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class AuthDummyUserView(GenericAPIView):
    serializer_class = NoneSerializer
    permission_classes = ()

    def post(self, request):
        user = User.objects.create_guest_user()
        user.name = 'dummy user'
        user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = TokenOutputSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

