from rest_framework import serializers

from ..checks.instructor_comment_check import InstructorCommentCheck
from ..models.instructor_comment import InstructorComment


class InstructorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorComment
        fields = '__all__'

    def validate(self, data):
        form = InstructorCommentCheck(data)

        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)
