from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            # Cherche un utilisateur avec l'email OU le nom d'utilisateur
            user = user_model.objects.get(Q(username=username) | Q(email=email))
        except user_model.DoesNotExist:
            return None
        except user_model.MultipleObjectsReturned:
            return None

        if user.check_password(password):
            return user
        return None
