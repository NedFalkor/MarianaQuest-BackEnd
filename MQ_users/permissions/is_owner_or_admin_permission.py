from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Les administrateurs peuvent modifier tout profil
        if request.user.is_superuser:
            return True

        # Les utilisateurs ne peuvent modifier que leur propre profil
        return obj.user == request.user
