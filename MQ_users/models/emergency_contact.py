from django.db import models

from MQ_users.models import DiverProfile


class EmergencyContact(models.Model):
    last_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True)
    diver_profile = models.ForeignKey(DiverProfile, on_delete=models.CASCADE, related_name='emergency_contacts',
                                      null=True)

    def __str__(self):
        return f"Emergency Contact - {self.first_name} {self.last_name}"
