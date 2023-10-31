from rest_framework import serializers

from MQ_users.models.custom_user import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']