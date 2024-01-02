from rest_framework import permissions
from MQ_diving_logs.models.diving_log import DivingLog


class StatusPermission(permissions.BasePermission):
    message = "Only instructors can change the status."

    def has_object_permission(self, request, view, obj):
        # Tout le monde peut lire, mais la modification nécessite des conditions spécifiques
        if request.method in permissions.SAFE_METHODS:
            return True

        # Seuls les instructeurs peuvent changer le statut et uniquement si le statut n'est pas déjà 'VALIDATED'
        if isinstance(obj, DivingLog) and obj.status != 'VALIDATED':
            return request.user.is_instructor

        return False
