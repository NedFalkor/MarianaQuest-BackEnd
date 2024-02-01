from django.db import models
from django.contrib.auth.models import User

from MQ_users.models import CustomUser


class DiverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    identity_photo = models.ImageField(upload_to='identity_photos/', null=True, blank=True)

    last_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Profile of diver {self.user.username if self.user else 'unknown'}"
