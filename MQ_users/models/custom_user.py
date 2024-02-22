from AptUrl.Helpers import _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Le champ Email doit être renseigné'))
        if not username:
            raise ValueError(_('Le champ Username doit être renseigné'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('SuperUser doit avoir is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('SuperUser doit avoir is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    # Assume we want to keep the unique email field
    email = models.EmailField(_('email address'), unique=True)
    # Roles
    ROLE_CHOICES = [
        ('DIVER', 'Diver'),
        ('INSTRUCTOR', 'Instructor'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='DIVER')

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Requis. 150 caractères ou moins.'),
        error_messages={
            'unique': _("Un utilisateur avec ce nom d'utilisateur existe déjà."),
        },
    )
    date_created = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"
