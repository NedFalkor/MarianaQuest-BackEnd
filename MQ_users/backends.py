from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_model()
        try:
            if '@' in username:
                user = user.objects.get(email=username)
            else:
                user = user.objects.get(username=username)
        except user.DoesNotExist:
            return None

        if user.check_password(password):
            return user
