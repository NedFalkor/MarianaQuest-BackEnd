from django.db import models
from MQ_users.models import CustomUser
from MQ_users.models.dive_group import DiveGroup


class DivingLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dive_number = models.IntegerField(null=True, verbose_name="Dive Number")
    dive_date = models.DateField(null=True, verbose_name="Dive Date")
    dive_site = models.CharField(max_length=255, verbose_name="Dive Site")
    dive_group = models.ForeignKey(DiveGroup, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="Dive Group")
    objects = models.Manager()

    ENVIRONMENT_CHOICES = [
        ('sea', 'Sea'),
        ('ocean', 'Ocean'),
        ('lake', 'Lake'),
    ]
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICES, verbose_name="Environment")
    depth = models.FloatField(null=True, verbose_name="Depth (m)")
    duration_dive = models.IntegerField(null=True, verbose_name="Dive Duration (min)")
    surface_return = models.CharField(max_length=255, verbose_name="Surface Return (h/min)")
    decompression_stop = models.CharField(max_length=255, verbose_name="Decompression Stop")

    # Equipement
    BOTTLE_TYPE_CHOICES = [
        ('6l', '6 Liters'),
        ('12l', '12 Liters'),
        ('15l', '15 Liters'),
    ]
    bottle_type = models.CharField(max_length=3, choices=BOTTLE_TYPE_CHOICES, verbose_name="Bottle Type")

    WET_SUIT_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    wet_suit = models.CharField(max_length=2, choices=WET_SUIT_CHOICES, verbose_name="Wet Suit")
    ballast = models.CharField(max_length=255, verbose_name="Ballast")

    DIVE_TYPE_CHOICES = [
        ('training', 'Training'),
        ('exploration', 'Exploration'),
        ('night', 'Night dive'),
        ('drift', 'Drift dive'),
        ('wreck', 'Wreck'),
        ('other', 'Other'),
    ]
    dive_type = models.CharField(max_length=15, choices=DIVE_TYPE_CHOICES, verbose_name="Dive Type")

    GAS_TYPE_CHOICES = [
        ('nitrox', 'Nitrox'),
        ('trimix', 'Trimix'),
        ('rebreather', 'Rebreather'),
    ]
    gas_type = models.CharField(max_length=12, choices=GAS_TYPE_CHOICES, verbose_name="Gas Type")

    group = models.CharField(max_length=255, verbose_name="Group")
    consumption_start = models.IntegerField(null=True, verbose_name="Consumption Start")
    consumption_end = models.IntegerField(null=True, verbose_name="Consumption End")

    # Conditions
    air_temperature = models.FloatField(null=True, verbose_name="Air Temperature")
    water_temperature = models.FloatField(null=True, verbose_name="Water Temperature")

    VISIBILITY_CHOICES = [
        ('bad', 'Bad'),
        ('medium', 'Medium'),
        ('good', 'Good'),
    ]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, verbose_name="Visibility")

    CURRENT_CHOICES = [
        ('none', 'None'),
        ('weak', 'Weak'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]
    current = models.CharField(max_length=10, choices=CURRENT_CHOICES, verbose_name="Current")

    WEATHER_CHOICES = [
        ('sun', 'Sun'),
        ('cloud', 'Cloud'),
        ('rain', 'Rain'),
        ('downpour', 'Downpour')
    ]
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, verbose_name="Weather")
    WIND_CHOICES = [
        ('none', 'None'),
        ('weak', 'Weak'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]
    wind = models.CharField(max_length=10, choices=WIND_CHOICES, verbose_name="Wind")

    observations = models.TextField(blank=True, verbose_name="Observations")

    # Statut et validation
    STATUS_CHOICES = [
        ('AWAITING', 'Awaiting'),
        ('VALIDATED', 'Validated'),
        ('REFUSED', 'Refused'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AWAITING')
    validated_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='validated_dives')

    def __str__(self):
        return (f"Dive {self.dive_number or 'Unknown'} at {self.dive_site or 'Unknown Site'} "
                f"by {self.user.username if hasattr(self.user, 'username') else 'Unknown User'}")
