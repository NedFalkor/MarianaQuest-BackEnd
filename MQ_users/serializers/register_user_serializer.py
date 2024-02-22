from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError

from MQ_users.models.custom_user import CustomUser
from MQ_users.validators.custom_user_validator import CustomUserValidator


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

    def validate(self, data):
        # Assurez-vous qu'au moins l'email ou le nom d'utilisateur est fourni
        if not data.get('email') and not data.get('username'):
            raise serializers.ValidationError("Un e-mail ou un nom d'utilisateur doit être fourni.")

        # Utiliser CustomUserValidator pour valider l'email et le username
        custom_user_validator = CustomUserValidator(data=data)
        if not custom_user_validator.is_valid():
            raise ValidationError(custom_user_validator.errors)

        # Vérifiez si les mots de passe correspondent
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Les mots de passe ne correspondent pas."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        with transaction.atomic():
            # Créez l'utilisateur avec l'email et/ou le nom d'utilisateur
            user = CustomUser.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()

        return user
