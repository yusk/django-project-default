def is_logined(request):
    return {"is_logined": request.user.is_authenticated}


def logined_user(request):
    user = request.user if request.user.is_authenticated else None
    return {"logined_user": user}
