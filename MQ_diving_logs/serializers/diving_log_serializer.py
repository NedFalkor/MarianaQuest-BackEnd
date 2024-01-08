from rest_framework import serializers

from MQ_diving_logs.checks.diving_log_check import DivingLogCheck
from MQ_diving_logs.models.diving_log import DivingLog


class DivingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivingLog
        fields = '__all__'

    def validate(self, data):
        form = DivingLogCheck(data)

        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)

    def validate_status(self, value):
        if not self.instance and value != 'AWAITING':
            raise serializers.ValidationError("Initial status must be 'AWAITING'")
        return value
