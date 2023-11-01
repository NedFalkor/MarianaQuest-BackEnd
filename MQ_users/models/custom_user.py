from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if email is None and username is None:
            raise ValueError('L’un des champs (email ou nom d’utilisateur) est obligatoire.')

        if email:
            email = self.normalize_email(email)
            extra_fields["email"] = email

        if username:
            extra_fields["username"] = username

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, username=username, password=password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Roles
    ROLE_CHOICES = [
        ('PLONGEUR', 'Plongeur'),
        ('FORMATEUR', 'Formateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLONGEUR')

    # Définition du manager personnalisé pour ce modèle
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.username
