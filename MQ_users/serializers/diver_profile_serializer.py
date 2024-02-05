from rest_framework import serializers

from MQ_users.checks.diver_profile_check import DiverProfileCheck
from MQ_users.models import DiverProfile, EmergencyContact
from MQ_users.serializers.emergency_contact_serializer import EmergencyContactSerializer


class DiverProfileSerializer(serializers.ModelSerializer):
    emergency_contact = EmergencyContactSerializer()
    role = serializers.ReadOnlyField(source='user.role')

    class Meta:
        model = DiverProfile
        fields = '__all__'

    def validate(self, data):
        form = DiverProfileCheck(data)

        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)

    def create(self, validated_data):
        emergency_contact_data = validated_data.pop('emergency_contact')
        diver_profile = DiverProfile.objects.create(**validated_data)
        EmergencyContact.objects.create(diver_profile=diver_profile, **emergency_contact_data)
        return diver_profile

    def update(self, instance, validated_data):
        emergency_contact_data = validated_data.pop('emergency_contact')
        emergency_contact = instance.emergency_contact

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        for key, value in emergency_contact_data.items():
            setattr(emergency_contact, key, value)
        emergency_contact.save()

        return instance
