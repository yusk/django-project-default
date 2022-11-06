import traceback

from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.serializers import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = DRFValidationError(exc.message_dict)
    elif isinstance(exc, IntegrityError):
        traceback.print_exc()
        exc = DRFValidationError(
            {"message": "入力が許可されたものではありません。記入した情報を今一度ご確認ください。"})
    return exception_handler(exc, context)
