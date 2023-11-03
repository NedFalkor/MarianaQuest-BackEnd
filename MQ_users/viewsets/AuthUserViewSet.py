from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout

from MQ_users.serializers.AuthUserSerializer import AuthUserSerializer

class AuthUserViewSet(viewsets.ViewSet):
    serializer_class = AuthUserSerializer
    permission_classes = [IsAuthenticated]

    @classmethod
    def get_extra_actions(cls):
        return []

    def get_permissions(self):
        if self.action == 'login':
            return []
        return [IsAuthenticated()]

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user:
            login(request, user)
            return Response({"message": "Connecté avec succès"}, status=status.HTTP_200_OK)
        return Response({"error": "Erreur de connexion"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['DELETE'])
    def destroy(self, request):
        # Delete the authenticated user
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
