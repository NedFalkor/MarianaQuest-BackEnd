from django.contrib import admin
from .models import CustomUser, DiverProfile, EmergencyContact
from .models.dive_group import DiveGroup


class DiverProfileInline(admin.StackedInline):
    model = DiverProfile
    can_delete = False
    verbose_name_plural = 'Diver Profiles'
    fk_name = 'user'


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
        'get_username', 'get_email', 'get_role', 'last_name', 'first_name',
        'address', 'postal_code', 'city', 'country', 'landline', 'mobile',
        'get_emergency_contact_name', 'get_emergency_contact_phone'
    )
    search_fields = (
        'user__username', 'user__email', 'last_name', 'first_name',
        'address', 'postal_code', 'city', 'country', 'landline', 'mobile',
        'emergency_contacts__last_name', 'emergency_contacts__mobile'
    )
    list_filter = ('user__role', 'last_name', 'first_name')
    inlines = [EmergencyContactInline]

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = 'user__username'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    def get_role(self, obj):
        return obj.user.role

    get_role.admin_order_field = 'user__role'
    get_role.short_description = 'Role'

    def get_emergency_contact_name(self, obj):
        contacts = obj.emergency_contacts.all()
        if contacts:
            return contacts[0].last_name
        return '-'

    get_emergency_contact_name.short_description = 'Emergency Contact Name'

    def get_emergency_contact_phone(self, obj):
        contacts = obj.emergency_contacts.all()
        if contacts:
            return contacts[0].mobile
        return '-'

    get_emergency_contact_phone.short_description = 'Emergency Contact Phone'

    @admin.register(EmergencyContact)
    class EmergencyContactAdmin(admin.ModelAdmin):
        list_display = ('diver_profile', 'last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
        search_fields = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
        list_filter = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
