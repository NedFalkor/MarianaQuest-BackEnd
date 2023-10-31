from django.db import models


class EmergencyContact(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    address = models.TextField()
    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f"Emergency Contact - {self.first_name} {self.last_name}"
