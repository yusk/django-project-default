from django.conf import settings

from main.env import IGNORE_GOOGLE_ANALYTICS


def debug(request):
    return {"debug": settings.DEBUG}


def ignore_google_analytics(request):
    return {"ignore_google_analytics": IGNORE_GOOGLE_ANALYTICS}


def is_logged_in(request):
    return {"is_logged_in": request.user.is_authenticated}


def logged_in_user(request):
    user = request.user if request.user.is_authenticated else None
    return {"logged_in_user": user}
