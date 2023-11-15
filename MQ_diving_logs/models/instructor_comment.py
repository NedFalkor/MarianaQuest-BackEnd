from django.db import models

from MQ_users.models import CustomUser
from .diving_log import DivingLog


class InstructorComment(models.Model):
    diving_log = models.ForeignKey(DivingLog, on_delete=models.CASCADE)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Comment")
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return (
            f"Comment by {self.instructor.username if hasattr(self.instructor, 'username') else 'Unknown Instructor'}"
            f" on {self.comment_date}")
