from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import CustomUser


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    CustomUser.objects.filter(pk=user.pk).update(is_online=True)


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    CustomUser.objects.filter(pk=user.pk).update(is_online=False)
