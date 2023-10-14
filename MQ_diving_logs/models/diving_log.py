from django.db import models


class DivingLog(models.Model):
    # Paramètres
    dive_number = models.IntegerField(null=True, blank=True, verbose_name="Dive Number")
    dive_date = models.DateField(null=True, blank=True, verbose_name="Dive Date")
    dive_site = models.CharField(max_length=255, blank=True, verbose_name="Dive Site")

    ENVIRONMENT_CHOICES = [
        ('sea', 'Sea'),
        ('ocean', 'Ocean'),
        ('lake', 'Lake'),
    ]
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICES, blank=True, verbose_name="Environment")
    depth = models.FloatField(null=True, blank=True, verbose_name="Depth (m)")
    duration_dive = models.IntegerField(null=True, blank=True, verbose_name="Dive Duration (min)")
    surface_return = models.CharField(max_length=255, blank=True, verbose_name="Surface Return (h/min)")
    decompression_stop = models.CharField(max_length=255, blank=True, verbose_name="Decompression Stop")

    # Equipement
    bottle_type = models.IntegerField(null=True, blank=True, verbose_name="Bottle Type")
    wet_suit = models.CharField(max_length=255, blank=True, verbose_name="Wet Suit")
    ballast = models.CharField(max_length=255, blank=True, verbose_name="Ballast")

    DIVE_TYPE_CHOICES = [
        ('training', 'Training'),
        ('exploration', 'Exploration'),
        ('night', 'Night dive'),
        ('drift', 'Drift dive'),
        ('wreck', 'Wreck'),
        ('other', 'Other'),
    ]
    dive_type = models.CharField(max_length=15, choices=DIVE_TYPE_CHOICES, blank=True, verbose_name="Dive Type")

    GAS_TYPE_CHOICES = [
        ('nitrox', 'Nitrox'),
        ('trimix', 'Trimix'),
        ('rebreather', 'Rebreather'),
    ]
    gas_type = models.CharField(max_length=12, choices=GAS_TYPE_CHOICES, blank=True, verbose_name="Gas Type")

    group = models.CharField(max_length=255, blank=True, verbose_name="Group")
    consumption_start = models.IntegerField(null=True, blank=True, verbose_name="Consumption Start")
    consumption_end = models.IntegerField(null=True, blank=True, verbose_name="Consumption End")

    # Conditions
    air_temperature = models.FloatField(null=True, blank=True, verbose_name="Air Temperature")
    water_temperature = models.FloatField(null=True, blank=True, verbose_name="Water Temperature")

    WEATHER_CHOICES = [
        ('sun', 'Sunny'),
        ('cloud', 'Cloudy'),
        ('rain', 'Rain'),
        ('downpour', 'Downpour'),
    ]
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, blank=True, verbose_name="Weather")
    visibility = models.CharField(max_length=255, blank=True, verbose_name="Visibility")
    current = models.CharField(max_length=255, blank=True, verbose_name="Current")
    observations = models.TextField(blank=True, verbose_name="Observations")

    # Signature & Stamp
    signature_data = models.ImageField(upload_to='signatures/', null=True, blank=True, verbose_name="Signature Data")
    stamp_preview = models.ImageField(upload_to='stamps/', null=True, blank=True, verbose_name="Stamp Preview")

    def __str__(self):
        return f"Dive {self.dive_number or 'Unknown'} at {self.dive_site or 'Unknown Site'}"
