from rest_framework import serializers
from MQ_diving_logs.models.diving_log import DivingLog


class DivingLogSerializer(serializers.ModelSerializer):
    dive_number = serializers.IntegerField(allow_null=True, required=False)
    dive_date = serializers.DateField(allow_null=True, required=False)
    dive_site = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = DivingLog
        fields = '__all__'

