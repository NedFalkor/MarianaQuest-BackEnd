from rest_framework import serializers

from MQ_users.models.dive_group import DiveGroup


class DiveGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiveGroup
        fields = '__all__'
