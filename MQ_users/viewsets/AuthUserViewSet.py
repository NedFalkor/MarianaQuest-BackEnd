from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout

from MQ_users.serializers.AuthUserSerializer import AuthUserSerializer
from django.core.exceptions import ValidationError


class AuthUserViewSet(viewsets.ViewSet):
    serializer_class = AuthUserSerializer

    def get_permissions(self):
        if self.action in ['login', 'logout']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming that your AuthUserSerializer now accepts both email and username
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Custom logic to authenticate by email and username could be implemented here.
        # For example:
        user = authenticate(request, email=email, username=username, password=password)
        if not user:
            raise ValidationError('Invalid login credentials.')

        login(request, user)
        return Response({"message": "Connecté avec succès"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def logout(self, request):
        logout(request)
        return Response({"message": "Déconnecté avec succès"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        # Delete the authenticated user
        request.user.delete()
        return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)

