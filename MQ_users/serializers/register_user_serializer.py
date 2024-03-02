from rest_framework import serializers
from django.db import transaction
from MQ_users.models.custom_user import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
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
        # Au moins l'email ou le nom d'utilisateur est fourni
        if not data.get('email') and not data.get('username'):
            raise serializers.ValidationError("Un e-mail ou un nom d'utilisateur doit être fourni.")

        # Unicité de l'email et du nom d'utilisateur si fournis
        email = data.get('email')
        username = data.get('username')
        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Un utilisateur avec cet e-mail existe déjà."})
        if username and CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Un utilisateur avec ce nom d'utilisateur existe déjà."})

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
