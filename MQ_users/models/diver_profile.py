from django.db import models

from MQ_users.models import CustomUser

ROLE_CHOICES = (
    ('PLONGEUR', 'Plongeur'),
    ('FORMATEUR', 'Formateur'),
)


class DiverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    logbook_number = models.CharField(max_length=255)
    cumulative_dives_in_logbook = models.PositiveIntegerField()
    total_dives = models.PositiveIntegerField()
    identity_photo = models.ImageField(upload_to='identity_photos/', null=True, blank=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLONGEUR')

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()

    emergency_contact = models.ForeignKey('EmergencyContact', on_delete=models.CASCADE, null=True,
                                          blank=True)

    def __str__(self):
        return f"Profile of diver {self.user.username if self.user else 'unknown'} - Logbook No. {self.logbook_number}"
