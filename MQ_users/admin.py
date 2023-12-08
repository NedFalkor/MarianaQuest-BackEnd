from django.contrib import admin
from .models import CustomUser, DiverProfile, EmergencyContact
from .models.dive_group import DiveGroup


class EmergencyContactInline(admin.StackedInline):
    model = EmergencyContact
    extra = 1


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


@admin.register(DiverProfile)
class DiverProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'last_name', 'first_name', 'email', 'address', 'postal_code', 'city', 'country', 'landline', 'mobile')
    search_fields = ('last_name',
                     'first_name', 'email', 'address', 'postal_code', 'city', 'country', 'landline', 'mobile')
    list_filter = ('last_name', 'first_name')
    inlines = [EmergencyContactInline]

    @admin.register(EmergencyContact)
    class EmergencyContactAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
        search_fields = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
        list_filter = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
