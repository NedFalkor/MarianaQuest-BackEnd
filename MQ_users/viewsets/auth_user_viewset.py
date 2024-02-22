from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from MQ_users.serializers.auth_user_serializer import AuthUserSerializer


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

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        refresh['username'] = user.username
        refresh['role'] = user.role
        refresh['user_id'] = user.id

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def logout(self, request):
        logout(request)
        response = Response({"message": "Déconnecté avec succès"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        return response

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        # Invalidate all refresh tokens
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            _, created = BlacklistedToken.objects.get_or_create(token=token)

        request.user.delete()
        return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
