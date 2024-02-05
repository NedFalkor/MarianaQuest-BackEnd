from rest_framework import permissions
from MQ_diving_logs.models.diving_log import DivingLog


class StatusPermission(permissions.BasePermission):
    message = "Only instructors can change the status."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, DivingLog) and obj.status != 'VALIDATED':
            if hasattr(request.user, 'is_instructor') and request.user.is_instructor:
                return True
            else:
                # Optionally, you can raise an exception here with the custom message
                self.message = "Only instructors can change the status and the status must not be 'VALIDATED'."
                return False
        return False
