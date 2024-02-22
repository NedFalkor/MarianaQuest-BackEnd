from django.db import models

from MQ_users.models import DiverProfile


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    landline = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    diver_profile = models.OneToOneField(
        DiverProfile,
        on_delete=models.CASCADE,
        related_name='emergency_contact'
    )

    def __str__(self):
        return f"Emergency Contact - {self.first_name} {self.last_name}"
