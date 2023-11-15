from django.db import models
from MQ_users.models import CustomUser


class DivingLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dive_number = models.IntegerField(null=True, blank=True, verbose_name="Dive Number")
    dive_date = models.DateField(null=True, blank=True, verbose_name="Dive Date")
    dive_site = models.CharField(max_length=255, blank=True, verbose_name="Dive Site")
    objects = models.Manager()

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
    BOTTLE_TYPE_CHOICES = [
        ('6l', '6 Liters'),
        ('12l', '12 Liters'),
        ('15l', '15 Liters'),
    ]
    bottle_type = models.CharField(max_length=3, choices=BOTTLE_TYPE_CHOICES, blank=True, verbose_name="Bottle Type")

    WET_SUIT_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    wet_suit = models.CharField(max_length=2, choices=WET_SUIT_CHOICES, blank=True, verbose_name="Wet Suit")
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

    VISIBILITY_CHOICES = [
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('bonne', 'Bonne'),
    ]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, blank=True, verbose_name="Visibility")

    CURRENT_CHOICES = [
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('fort', 'Fort'),
    ]
    current = models.CharField(max_length=10, choices=CURRENT_CHOICES, blank=True, verbose_name="Current")

    WEATHER_CHOICES = [
        ('soleil', 'Soleil'),
        ('nuage', 'Nuage'),
        ('pluie', 'Pluie'),
        ('averse', 'Averse')
    ]
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, blank=True, verbose_name="Weather")
    WIND_CHOICES = [
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('fort', 'Fort'),
    ]
    wind = models.CharField(max_length=10, choices=WIND_CHOICES, blank=True, verbose_name="Wind")

    observations = models.TextField(blank=True, verbose_name="Observations")

    # Signature & Stamp
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True, verbose_name="Signature")
    stamp = models.ImageField(upload_to='stamps/', null=True, blank=True, verbose_name="Stamp")

    # Statut et validation
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDÉ', 'Validé'),
        ('REFUSÉ', 'Refusé'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='EN_ATTENTE')
    validated_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='validated_dives')

    def __str__(self):
        return (f"Dive {self.dive_number or 'Unknown'} at {self.dive_site or 'Unknown Site'} "
                f"by {self.user.username if hasattr(self.user, 'username') else 'Unknown User'}")
