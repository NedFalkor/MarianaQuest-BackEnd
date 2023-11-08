from rest_framework import serializers
from MQ_users.models.custom_user import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    email_or_username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'},
                                             min_length=8)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email_or_username', 'password', 'confirm_password', 'role']

    def validate(self, data):
        email_or_username = data['email_or_username']
        if "@" in email_or_username and "." in email_or_username:
            data['email'] = email_or_username
        else:
            data['username'] = email_or_username

        # Check if passwords match.
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Les mots de passe ne correspondent pas."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        validated_data.pop('email_or_username', None)

        user = CustomUser.objects.create_user(**validated_data)
        return user
