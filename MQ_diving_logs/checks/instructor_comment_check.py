from django import forms
from django.core.exceptions import ValidationError
from MQ_diving_logs.models.instructor_comment import InstructorComment
from MQ_diving_logs.models.diving_log import DivingLog
from datetime import datetime


class InstructorCommentCheck(forms.ModelForm):
    class Meta:
        model = InstructorComment
        fields = '__all__'

    def clean_diving_log(self):
        diving_log = self.cleaned_data.get('diving_log')
        if diving_log and diving_log.status != 'AWAITING':
            raise forms.ValidationError(
                "Instructor comments can only be added when the diving log is in 'AWAITING' status.")
        return diving_log

    def clean_comment_date(self):
        comment_date = self.cleaned_data.get('comment_date')
        if comment_date and comment_date > datetime.now():
            raise forms.ValidationError("Comment date cannot be in the future.")
        return comment_date

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get('instructor')
        diving_log = cleaned_data.get('diving_log')

        if diving_log and instructor and diving_log.user == instructor:
            raise ValidationError("Instructor cannot comment on their own diving log.")

        return cleaned_data
