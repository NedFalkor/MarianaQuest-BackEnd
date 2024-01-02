from rest_framework import permissions


class IsDiver(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'DIVER'
