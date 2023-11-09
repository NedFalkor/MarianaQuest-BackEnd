from AptUrl.Helpers import _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    # Assume we want to keep the unique email field
    email = models.EmailField(_('email address'), unique=True)

    # Roles
    ROLE_CHOICES = [
        ('PLONGEUR', 'Plongeur'),
        ('FORMATEUR', 'Formateur'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLONGEUR')

    # Définition du manager personnalisé pour ce modèle
    objects = CustomUserManager()

    # Utilisez à la fois l'email et le nom d'utilisateur pour l'authentification
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"


# Nouveau modèle pour la palanquée (Dive Group)
class DiveGroup(models.Model):
    group_number = models.IntegerField(unique=True, verbose_name="Group Number")
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="led_dive_groups",
                               verbose_name="Group Leader")
    members = models.ManyToManyField(CustomUser, related_name="dive_groups", verbose_name="Group Members")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    def __str__(self):
        return f"Group {self.group_number} led by {self.leader.username}"
