from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailAndUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            # Check for a user with the given username and email
            user = user_model.objects.get(username=username, email=email)
        except user_model.DoesNotExist:
            return None
        except user_model.MultipleObjectsReturned:
            return None

        if user.check_password(password):
            return user
        return None
