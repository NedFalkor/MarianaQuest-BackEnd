from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers.RegisterUserSerializer import RegisterUserSerializer


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]  # Seuls les utilisateurs non authentifiés peuvent accéder

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        response = super(RegisterUserViewSet, self).create(request, *args, **kwargs)

        # Après avoir créé un utilisateur, vous pouvez ajouter des étapes supplémentaires,
        # comme créer un profil DiverProfile associé.
        # Exemple: DiverProfile.objects.create(user=response.data['id'])

        return response
