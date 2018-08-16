from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login

from main.forms import SignupForm, SigninForm


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
