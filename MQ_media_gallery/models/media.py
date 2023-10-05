# MQ_media_gallery/models.py
from django.db import models
from MQ_users.models import User
from durationfield.db.models.fields.duration import DurationField

class Media(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media_gallery/', blank=True, null=True)
    video = models.FileField(upload_to='media_gallery/videos/', blank=True, null=True)
    duration = DurationField(blank=True, null=True)  # Pour stocker la durée de la vidéo.
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
