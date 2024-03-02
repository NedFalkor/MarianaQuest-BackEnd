from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.permissions.is_diver_permission import IsDiver
from MQ_diving_logs.permissions.is_instructor_permission import IsInstructor
from MQ_diving_logs.serializers.diving_log_serializer import DivingLogSerializer
from MQ_users.models import CustomUser


class DivingLogViewSet(viewsets.ModelViewSet):
    queryset = DivingLog.objects.all()
    serializer_class = DivingLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        diver_id = self.request.query_params.get('diver_id', None)
        if diver_id is not None:
            queryset = queryset.filter(diver=diver_id)
        return queryset

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsDiver()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsInstructor])
    def validate_log(self, request, pk=None):
        try:
            diving_log = self.get_object()
            diving_log.status = 'VALIDATED'
            diving_log.validated_by = request.user
            diving_log.save(update_fields=['status', 'validated_by'])
            return Response({"message": "Diving log has been validated."})
        except ObjectDoesNotExist:
            return Response({"error": "Diving log not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            # You could add a check here to ensure the user exists before creating a DivingLog
            user_id = request.data.get('user')
            if not CustomUser.objects.filter(id=user_id).exists():
                raise ValidationError(f"User with id {user_id} does not exist.")

            request.data['status'] = 'AWAITING'  # Set initial status to 'AWAITING'
            response = super().create(request, *args, **kwargs)
            return response
        except ValidationError as e:
            return Response({"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # It is generally not a good practice to catch generic Exceptions without re-raising.
            # Consider logging the error and perhaps reraising a more specific exception.
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        user = request.user
        try:
            instance = self.get_object()

            if hasattr(user, 'role') and user.role != 'INSTRUCTOR':
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"message": "Only instructors can modify status"})

            return super().update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({"error": "Diving log not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        try:
            if hasattr(user, 'role') and user.role != 'INSTRUCTOR':
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"message": "Only instructors can delete a log"})

            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({"error": "Diving log not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
