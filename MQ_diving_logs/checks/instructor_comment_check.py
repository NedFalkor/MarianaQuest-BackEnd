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
                    "Les commentaires de l'instructeur ne peuvent être ajoutés que lorsque le journal de plongée est à "
                    "l'état « EN ATTENTE ».")
            if diving_log.user.role != 'DIVER':
                raise forms.ValidationError(
                    "Les commentaires de l'instructeur ne peuvent être faits que sur les journaux de plongée des "
                    "utilisateurs ayant le rôle « PLONGEUR ».")
        return diving_log

    def clean_comment_date(self):
        comment_date = self.cleaned_data.get('comment_date')
        diving_log_date = self.cleaned_data.get('diving_log').dive_date if self.cleaned_data.get('diving_log') else None

        if comment_date and diving_log_date and comment_date < diving_log_date:
            raise forms.ValidationError("La date du commentaire ne peut pas être antérieure à la date de la plongée.")
        if comment_date and comment_date > datetime.now():
            raise forms.ValidationError("La date du commentaire ne peut pas être postérieure.")
        return comment_date

    def clean_instructor(self):
        instructor = self.cleaned_data.get('instructor')
        if instructor and instructor.role != 'INSTRUCTOR':
            raise forms.ValidationError("Seuls les utilisateurs ayant le rôle «INSTRUCTEUR» peuvent faire des "
                                        "commentaires.")
        return instructor

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get('instructor')
        diving_log = cleaned_data.get('diving_log')
        signature = cleaned_data.get('signature')
        stamp = cleaned_data.get('stamp')

        if diving_log and instructor and diving_log.user == instructor:
            raise ValidationError("L'instructeur ne peut pas commenter son propre journal de plongée.")

        if not signature or not stamp:
            raise ValidationError("La signature et le cachet sont requis.")

        return cleaned_data
