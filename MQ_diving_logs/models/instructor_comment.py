from django.db import models

from MQ_users.models import CustomUser
from .diving_log import DivingLog


class InstructorComment(models.Model):
    diving_log = models.ForeignKey(DivingLog, on_delete=models.CASCADE)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    # Signature & Stamp
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True, verbose_name="Signature")
    stamp = models.ImageField(upload_to='stamps/', null=True, blank=True, verbose_name="Stamp")

    def save(self, *args, **kwargs):
        if self.diving_log.status != 'AWAITING':
            raise ValueError("Instructor comments can only be added when the diving log is in 'AWAITING' status.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return (
            f"Comment by {self.instructor.username if hasattr(self.instructor, 'username') else 'Unknown Instructor'}"
            f" on {self.comment_date}")
