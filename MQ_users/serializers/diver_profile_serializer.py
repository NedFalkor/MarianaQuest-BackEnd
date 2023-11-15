from rest_framework import serializers

from MQ_users.models.diver_profile import DiverProfile
from MQ_users.serializers.emergency_contact_serializer import EmergencyContactSerializer


class DiverProfileSerializer(serializers.ModelSerializer):
    emergency_contact = EmergencyContactSerializer()

    class Meta:
        model = DiverProfile
        fields = '__all__'
