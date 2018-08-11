from django.contrib.auth import authenticate
from django.forms import Form
from django.forms.fields import EmailField, CharField
from django.forms.widgets import TextInput, PasswordInput
from django.core.exceptions import FieldError

from main.models import User


class ModelFormWithFormSetMixin:
    def __init__(self, form_kwargs={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset = self.formset_class(
            form_kwargs=form_kwargs,
            instance=self.instance,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
        )
        try:
            queryset = self.formset.queryset.order_by('created_at')
            queryset.first()
            self.formset = self.formset_class(
                form_kwargs=form_kwargs,
                instance=self.instance,
                data=self.data if self.is_bound else None,
                files=self.files if self.is_bound else None,
                queryset=queryset
            )
        except FieldError:
            pass

    def is_valid(self):
        return super().is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super().save(commit)
        self.formset.save(commit)
        return saved_instance


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f_name in self.fields.keys():
            self.fields[f_name].widget.attrs['class'] = 'form-control'


class SignupForm(BootstrapFormMixin, Form):
    name = CharField(
        max_length=256, required=True,
        widget=TextInput(
            attrs={'placeholder': 'ユーザーネーム'}))
    email = EmailField(
        max_length=256, required=True,
        widget=TextInput(
            attrs={'placeholder': 'メールアドレス'}))
    password = CharField(
        min_length=8, max_length=256, required=True,
        widget=PasswordInput(
            attrs={'placeholder': 'パスワード(8文字以上)'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_user(self):
        if 'name' in self.cleaned_data:
            name = self.cleaned_data['name']
        else:
            name = None
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = None
        try:
            if name:
                user = User.objects.create_user(email, password, name=name)
            else:
                user = User.objects.create_user(email, password)
        except:
            self.add_error('password', 'ユーザーの作成に失敗しました.')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            self.add_error('email', 'そのメールアドレスは既に使われています.')
        return email


class SigninForm(BootstrapFormMixin, Form):
    email = EmailField(
        max_length=256, required=True,
        widget=TextInput(
            attrs={'placeholder': 'メールアドレス'}))
    password = CharField(
        max_length=256, required=True,
        widget=PasswordInput(
            attrs={'placeholder': 'パスワード'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() == 0:
            self.add_error('password', 'メールアドレスかパスワードが正しくありません。')
        return email

    def get_authenticated_user(self):
        user = authenticate(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        if user is None:
            self.add_error('password', 'メールアドレスかパスワードが正しくありません。')
        return user
