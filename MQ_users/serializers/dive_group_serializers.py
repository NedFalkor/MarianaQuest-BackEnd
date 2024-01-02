from rest_framework import serializers

from MQ_users.models import CustomUser
from MQ_users.models.dive_group import DiveGroup


class DiveGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiveGroup
        fields = '__all__'

        # Ensure that the many-to-many field is properly represented
        divers = serializers.PrimaryKeyRelatedField(
            many=True, queryset=CustomUser.objects.filter(role='DIVER')
        )
