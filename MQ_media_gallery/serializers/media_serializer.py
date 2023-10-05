import subprocess

from rest_framework import serializers
from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

    def validate_video(self, value):
        # ffmpeg pour obtenir la durée de la vidéo
        result = subprocess.run(
            ['ffmpeg', '-i', value.path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
            stdout=subprocess.PIPE)

        # Convertit la durée en secondes / vérifie si elle dépasse 60s
        duration = float(result.stdout)
        if duration > 60:
            raise serializers.ValidationError("La vidéo dépasse la durée maximale autorisée de 1 minute.")

        return value
