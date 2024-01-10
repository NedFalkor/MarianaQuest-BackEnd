from rest_framework import permissions


class IsRelatedUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Les administrateurs ont tous les droits
        if request.user.is_superuser:
            return True

        # Les utilisateurs peuvent gérer les contacts d'urgence liés à leur profil
        return obj.diver_profile.user == request.user
