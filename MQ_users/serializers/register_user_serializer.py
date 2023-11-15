from rest_framework import serializers
from django.db import transaction
from MQ_users.models.custom_user import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password'},
                                     min_length=8)
    confirm_password = serializers.CharField(write_only=True,
                                             required=True,
                                             style={'input_type': 'password'},
                                             min_length=8)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES,
                                   write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password', 'role']
        # Removed the line that disables unique validator for username

    def validate_email(self, value):
        # Check if the email is already in use.
        if value and CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet e-mail existe déjà.")
        return value

    def validate_username(self, value):
        # Check if the username is already in use.
        if value and CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return value

    def validate(self, data):
        # Check if either email or username is provided
        if not data.get('email') and not data.get('username'):
            raise serializers.ValidationError("Un e-mail ou un nom d'utilisateur doit être fourni.")

        # Check if passwords match.
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Les mots de passe ne correspondent pas."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        with transaction.atomic():  # Ensure the database operation is atomic
            # Create the user with both email and username if provided
            user = CustomUser.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()

        return user
