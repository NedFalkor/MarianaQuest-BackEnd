from rest_framework import permissions
from MQ_diving_logs.models.diving_log import DivingLog


class StatusPermission(permissions.BasePermission):
    message = "Seuls les instructeurs peuvent modifier le statut."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, DivingLog) and obj.status != 'VALIDATED':
            if hasattr(request.user, 'is_instructor') and request.user.is_instructor:
                return True
            else:
                # Optionally, you can raise an exception here with the custom message
                self.message = ("Seuls les instructeurs peuvent modifier le statut et le statut ne doit pas être "
                                "« VALIDÉ ».")
                return False
        return False
