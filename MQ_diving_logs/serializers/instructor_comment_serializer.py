from rest_framework import serializers
from ..models.instructor_comment import InstructorComment


class InstructorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorComment
        fields = '__all__'
