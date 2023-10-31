# MQ_users/serializers/DiverProfileSerializer.py

from rest_framework import serializers

from MQ_users.models.diver_profile import DiverProfile


class DiverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiverProfile
        fields = '__all__'
