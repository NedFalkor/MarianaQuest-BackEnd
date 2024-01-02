from rest_framework import serializers
from MQ_diving_logs.models.diving_log import DivingLog


class DivingLogSerializer(serializers.ModelSerializer):
    dive_number = serializers.IntegerField(allow_null=True, required=False)
    dive_date = serializers.DateField(allow_null=True, required=False)
    dive_site = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = DivingLog
        fields = '__all__'

    def validate_status(self, value):
        # Si c'est une création (l'instance n'existe pas encore)
        if not self.instance:
            if value != 'VALIDATED':
                raise serializers.ValidationError("Initial status must be 'VALIDATED'")
        return value
