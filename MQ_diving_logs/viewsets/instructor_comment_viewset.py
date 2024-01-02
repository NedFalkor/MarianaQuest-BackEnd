from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from MQ_diving_logs.models.instructor_comment import InstructorComment
from MQ_diving_logs.permissions.is_instructor_or_adminpermission import IsInstructor
from MQ_diving_logs.serializers.instructor_comment_serializer import InstructorCommentSerializer


class InstructorCommentViewSet(viewsets.ModelViewSet):
    queryset = InstructorComment.objects.all()
    serializer_class = InstructorCommentSerializer
    permission_classes = [IsInstructor]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsInstructor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Vérifiez si l'utilisateur actuel est l'instructeur qui a créé le commentaire
        if instance.instructor != request.user:
            return Response({"error": "Not allowed to update this comment"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Vérifiez si l'utilisateur actuel est l'instructeur qui a créé le commentaire
        if instance.instructor != request.user:
            return Response({"error": "Not allowed to delete this comment"}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
