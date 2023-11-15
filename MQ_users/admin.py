from django.contrib import admin
from .models import CustomUser
from .models.dive_group import DiveGroup


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')


@admin.register(DiveGroup)
class DiveGroupAdmin(admin.ModelAdmin):
    list_display = ('group_number', 'boat_driver', 'trainer_one', 'trainer_two')
    search_fields = ('group_number', 'boat_driver__username', 'trainer_one__username', 'trainer_two__username')
    list_filter = ('boat_driver', 'trainer_one', 'trainer_two')

# Ajoutez d'autres modèles si nécessaire
