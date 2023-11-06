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
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLONGEUR')

    # Définition du manager personnalisé pour ce modèle
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.username


# Nouveau modèle pour la palanquée (Dive Group)
class DiveGroup(models.Model):
    group_number = models.IntegerField(unique=True, verbose_name="Group Number")
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="led_dive_groups",
                               verbose_name="Group Leader")
    members = models.ManyToManyField(CustomUser, related_name="dive_groups", verbose_name="Group Members")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    def __str__(self):
        return f"Group {self.group_number} led by {self.leader.username}"
