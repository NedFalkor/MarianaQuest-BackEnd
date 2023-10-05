from django.db import models
from django.contrib.auth.models import User

class DiverProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    logbook_number = models.CharField(max_length=255)
    cumulative_dives_in_logbook = models.PositiveIntegerField()
    total_dives = models.PositiveIntegerField()
    identity_photo = models.ImageField(upload_to='identity_photos/', null=True, blank=True)

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()

    emergency_contact_last_name = models.CharField(max_length=255)
    emergency_contact_first_name = models.CharField(max_length=255)
    emergency_contact_address = models.TextField()
    emergency_contact_landline = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_mobile = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_email = models.EmailField()

    def __str__(self):
        return f"Dive of {self.user.username} - {self.logbook_number}"
