from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers.user_profile_serializer import UserProfileSerializer


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # S'assurer que l'utilisateur ne peut accéder qu'à son propre profil
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        # Vérifiez si l'utilisateur actuel est celui qui effectue l'action
        if user != request.user:
            return Response({"error": "Not allowed to update this user"}, status=status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return super(UserProfileViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # Vérifiez si l'utilisateur actuel est un formateur
        if not hasattr(request.user, 'role') or request.user.role != 'FORMATEUR':
            return Response({"error": "Only trainers can delete a user"}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
