from rest_framework import serializers
from .models.diving_log import DivingLog


class DivingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivingLog
        fields = '__all__'
