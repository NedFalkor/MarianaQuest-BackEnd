from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.models.instructor_comment import InstructorComment
from MQ_diving_logs.permissions.is_diver_permission import IsDiver
from MQ_diving_logs.permissions.is_instructor_permission import IsInstructor
from MQ_diving_logs.permissions.status_permission import StatusPermission
from MQ_diving_logs.serializers.instructor_comment_serializer import InstructorCommentSerializer
from rest_framework import permissions


class InstructorCommentViewSet(viewsets.ModelViewSet):
    queryset = InstructorComment.objects.all()
    serializer_class = InstructorCommentSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role != 'INSTRUCTOR':
            queryset = queryset.none()  # Ceci assure que les utilisateurs non instructeurs ne voient aucun commentaire
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsDiver]
        elif self.action in ['validate_log', 'update', 'partial_update']:
            permission_classes = [IsInstructor, StatusPermission]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        diving_log_id = request.data.get('diving_log')
        diving_log = DivingLog.objects.filter(id=diving_log_id).first()

        # Check if the diving log exists
        if not diving_log:
            return Response({"error": "Diving log not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the diving log belongs to a diver
        if diving_log.user.role != 'DIVER':
            return Response({"error": "You can only comment on diving logs of divers."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the requesting user is an instructor
        if request.user.role != 'INSTRUCTOR':
            return Response({"error": "Only instructors can add comments."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the diving log status is 'AWAITING'
        if diving_log.status != 'AWAITING':
            return Response({"error": "Can only add comments to diving logs with 'AWAITING' status."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate and save the comment with the instructor set as the current user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
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
