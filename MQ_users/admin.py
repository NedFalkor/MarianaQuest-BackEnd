from django.contrib import admin

from MQ_users.models import DiverProfile, EmergencyContact, CustomUser
from MQ_users.models.dive_group import DiveGroup


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
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_created', 'is_online')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')


@admin.register(DiveGroup)
class DiveGroupAdmin(admin.ModelAdmin):
    list_display = (
        'group_description',
        'date',
        'boat_driver',
        'trainer_one',
        'trainer_two',
        'get_divers_list'
    )
    search_fields = ('group_description', 'boat_driver__username', 'trainer_one__username', 'trainer_two__username')
    list_filter = ('boat_driver', 'trainer_one', 'trainer_two')

    def boat_driver(self, obj):
        return obj.boat_driver.username if obj.boat_driver else '-'

    boat_driver.admin_order_field = 'boat_driver__username'
    boat_driver.short_description = 'Boat Driver'

    def trainer_one(self, obj):
        return obj.trainer_one.username if obj.trainer_one else '-'

    trainer_one.admin_order_field = 'trainer_one__username'
    trainer_one.short_description = 'First Trainer'

    def trainer_two(self, obj):
        return obj.trainer_two.username if obj.trainer_two else '-'

    trainer_two.admin_order_field = 'trainer_two__username'
    trainer_two.short_description = 'Second Trainer'

    def get_divers_list(self, obj):
        return ", ".join([diver.username for diver in obj.divers.all()]) if obj.divers.exists() else "-"

    get_divers_list.short_description = 'Divers'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.divers.set(form.cleaned_data.get('divers', []))


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

    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    def get_role(self, obj):
        return obj.user.role

    get_role.admin_order_field = 'user__role'
    get_role.short_description = 'Role'

    def get_emergency_contact_name(self, obj):
        contact = obj.emergency_contact
        return f"{contact.first_name} {contact.last_name}" if contact else '-'

    get_emergency_contact_name.short_description = 'EC Name'

    def get_emergency_contact_phone(self, obj):
        contact = obj.emergency_contact
        return contact.mobile if contact else '-'

    get_emergency_contact_phone.short_description = 'EC Phone'


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('diver_profile', 'last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
    search_fields = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
    list_filter = ('last_name', 'first_name', 'email', 'address', 'mobile', 'landline')
