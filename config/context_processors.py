from django.conf import settings


def debug(request):
    return {"debug": settings.DEBUG}


def ignore_google_analytics(request):
    return {"ignore_google_analytics": settings.IGNORE_GOOGLE_ANALYTICS}


def is_logined(request):
    return {"is_logined": request.user.is_authenticated}


def logined_user(request):
    user = request.user if request.user.is_authenticated else None
    return {"logined_user": user}
