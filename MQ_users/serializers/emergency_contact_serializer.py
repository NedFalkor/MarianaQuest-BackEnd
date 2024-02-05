from rest_framework import serializers

from MQ_users.checks.emergency_contact_check import EmergencyContactCheck
from MQ_users.models import EmergencyContact


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

    def validate(self, data):
        form = EmergencyContactCheck(data)

        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)
