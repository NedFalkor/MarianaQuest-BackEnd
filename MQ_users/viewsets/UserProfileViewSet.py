from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers.UserProfileSerializer import UserProfileSerializer


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return super(UserProfileViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
