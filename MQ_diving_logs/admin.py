from django.contrib import admin

from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.models.instructor_comment import InstructorComment


@admin.register(DivingLog)
class DivingLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DivingLog._meta.fields if field.name != "id"]
    search_fields = ('dive_number', 'dive_site', 'user__username', 'dive_group__group_number')
    list_filter = ('user', 'dive_date', 'dive_site', 'depth', 'environment', 'dive_type', 'status')

    # Si vous avez beaucoup de données, vous pouvez ajouter la pagination pour faciliter la navigation
    list_per_page = 25

    def get_dive_group_number(self, obj):
        return obj.dive_group.group_number if obj.dive_group else '-'
    get_dive_group_number.short_description = 'Dive Group Number'
    get_dive_group_number.admin_order_field = 'dive_group__group_number'


@admin.register(InstructorComment)
class InstructorCommentAdmin(admin.ModelAdmin):
    list_display = ('diving_log', 'instructor', 'comment', 'comment_date')
    list_filter = ('diving_log', 'instructor', 'comment_date')

    def has_add_permission(self, request, obj=None):
        # Only allow instructors to add comments
        return request.user.role == 'INSTRUCTOR'

    def has_change_permission(self, request, obj=None):
        # Only allow instructors to change their own comments
        if obj is not None and not request.user == obj.instructor:
            return False
        return request.user.role == 'INSTRUCTOR'

    def has_delete_permission(self, request, obj=None):
        # Only allow instructors to delete their own comments
        if obj is not None and not request.user == obj.instructor:
            return False
        return request.user.role == 'INSTRUCTOR'
