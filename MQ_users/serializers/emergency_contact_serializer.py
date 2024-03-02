from rest_framework import serializers

from MQ_users.models import EmergencyContact
from MQ_users.validators.emergency_contact_validator import EmergencyContactValidator


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

    def validate(self, data):
        form = EmergencyContactValidator(data)

        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)
