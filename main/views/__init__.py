from .auth import AuthUUIDView, AuthUserViewWithEmail  # noqa
from .confirm import ConfirmDigitView, ConfirmDigitResetView  # noqa
from .password import PasswordResetEmailView, PasswordResetDigitView, PasswordResetView  # noqa
from .register import RegisterDummyUserView, RegisterUUIDView, RegisterUserView, RegisterUserViewWithEmail  # noqa
from .status import StatusView  # noqa
from .user import UserView, UserViewSet, UserPasswordView  # noqa
