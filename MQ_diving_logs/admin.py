from django.contrib import admin

from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.models.instructor_comment import InstructorComment


@admin.register(DivingLog)
class DivingLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'dive_number', 'dive_date', 'dive_site', 'depth', 'duration_dive')
    list_filter = ('user', 'dive_date', 'dive_site', 'depth')


@admin.register(InstructorComment)
class InstructorCommentAdmin(admin.ModelAdmin):
    list_display = ('diving_log', 'instructor', 'comment', 'comment_date')
    list_filter = ('diving_log', 'instructor', 'comment_date')
