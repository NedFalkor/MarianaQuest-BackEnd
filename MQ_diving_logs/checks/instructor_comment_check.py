from django import forms
from django.core.exceptions import ValidationError
from MQ_diving_logs.models.instructor_comment import InstructorComment
from datetime import datetime


class InstructorCommentCheck(forms.ModelForm):
    class Meta:
        model = InstructorComment
        fields = '__all__'

    def clean_diving_log(self):
        diving_log = self.cleaned_data.get('diving_log')
        if diving_log:
            if diving_log.status != 'AWAITING':
                raise forms.ValidationError(
                    "Instructor comments can only be added when the diving log is in 'AWAITING' status.")
            if diving_log.user.role != 'DIVER':
                raise forms.ValidationError(
                    "Instructor comments can only be made on diving logs of users with the 'DIVER' role.")
        return diving_log

    def clean_comment_date(self):
        comment_date = self.cleaned_data.get('comment_date')
        diving_log_date = self.cleaned_data.get('diving_log').dive_date if self.cleaned_data.get('diving_log') else None

        if comment_date and diving_log_date and comment_date < diving_log_date:
            raise forms.ValidationError("Comment date cannot be before the dive date.")
        if comment_date and comment_date > datetime.now():
            raise forms.ValidationError("Comment date cannot be in the future.")
        return comment_date

    def clean_instructor(self):
        instructor = self.cleaned_data.get('instructor')
        if instructor and instructor.role != 'INSTRUCTOR':
            raise forms.ValidationError("Only users with the 'INSTRUCTOR' role can make comments.")
        return instructor

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get('instructor')
        diving_log = cleaned_data.get('diving_log')
        signature = cleaned_data.get('signature')
        stamp = cleaned_data.get('stamp')

        if diving_log and instructor and diving_log.user == instructor:
            raise ValidationError("Instructor cannot comment on their own diving log.")

        if not signature or not stamp:
            raise ValidationError("Signature and stamp are required.")

        return cleaned_data
