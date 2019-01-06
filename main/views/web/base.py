from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyLoginUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        room = request.user.get_active_room()
        if room is not None:
            if request.path.find(room.get_absolute_url()) < 0:
                return redirect(room.get_absolute_url())
        return super().get(request, *args, **kwargs)
