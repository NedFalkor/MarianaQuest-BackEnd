from django.db import models
from django.contrib.auth.models import User

from MQ_users.models import CustomUser


class DiverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    identity_photo = models.ImageField(upload_to='identity_photos/')

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    landline = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Profile of diver {self.user.username if self.user else 'unknown'}"
