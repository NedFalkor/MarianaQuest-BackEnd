from django.db import models

class DivingLog(models.Model):
    # Paramètres
    diveNumber = models.IntegerField(null=True, blank=True)
    diveDate = models.DateField(null=True, blank=True)
    diveSite = models.CharField(max_length=255, blank=True)
    ENVIRONMENT_CHOICES = [
        ('sea', 'Sea'),
        ('ocean', 'Ocean'),
        ('lake', 'Lake'),
    ]
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICES, blank=True)
    depth = models.FloatField(null=True, blank=True)
    durationDive = models.IntegerField(null=True, blank=True)
    surfaceReturn = models.CharField(max_length=255, blank=True)
    decompressionStop = models.CharField(max_length=255, blank=True)

    # Equipement
    bottleType = models.IntegerField(null=True, blank=True)
    wetSuit = models.CharField(max_length=255, blank=True)
    ballast = models.CharField(max_length=255, blank=True)
    DIVE_TYPE_CHOICES = [
        ('training', 'Training'),
        ('exploration', 'Exploration'),
        ('night', 'Night dive'),
        ('drift', 'Drift dive'),
        ('wreck', 'Wreck'),
        ('other', 'Other'),
    ]
    diveType = models.CharField(max_length=15, choices=DIVE_TYPE_CHOICES, blank=True)
    GAS_TYPE_CHOICES = [
        ('nitrox', 'Nitrox'),
        ('trimix', 'Trimix'),
        ('rebreather', 'Rebreather'),
    ]
    gasType = models.CharField(max_length=12, choices=GAS_TYPE_CHOICES, blank=True)
    group = models.CharField(max_length=255, blank=True)
    consumptionStart = models.IntegerField(null=True, blank=True)
    consumptionEnd = models.IntegerField(null=True, blank=True)

    # Conditions
    airTemperature = models.FloatField(null=True, blank=True)
    waterTemperature = models.FloatField(null=True, blank=True)
    WEATHER_CHOICES = [
        ('sun', 'Sunny'),
        ('cloud', 'Cloudy'),
        ('rain', 'Rain'),
        ('downpour', 'Downpour'),
    ]
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, blank=True)
    visibility = models.CharField(max_length=255, blank=True)
    current = models.CharField(max_length=255, blank=True)
    observations = models.TextField(blank=True)

    # Signature & Tampon
    signatureData = models.ImageField(upload_to='signatures/', null=True, blank=True)
    stampPreview = models.ImageField(upload_to='stamps/', null=True, blank=True)

    def __str__(self):
        return f"Dive {self.diveNumber} at {self.diveSite}"
