from django.db import models

from MQ_users.models import CustomUser
from MQ_users.models.dive_group import DiveGroup
from .diving_log import DivingLog


class InstructorComment(models.Model):
    diving_log = models.ForeignKey(DivingLog, on_delete=models.CASCADE)
    dive_group = models.ForeignKey(DiveGroup, on_delete=models.CASCADE, related_name='instructor_comments')
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    # Signature & Stamp
    signature = models.ImageField(upload_to='signatures/', verbose_name="Signature")
    stamp = models.ImageField(upload_to='stamps/', verbose_name="Stamp")

    def save(self, *args, **kwargs):
        if (self.instructor not in self.diving_log.dive_group.divers.all()
                and self.instructor != self.diving_log.dive_group.boat_driver):
            raise ValueError("Instructor must be part of the dive group.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return (
            f"Comment by {self.instructor.username if hasattr(self.instructor, 'username') else 'Instructeur inconnu'}"
            f" on {self.comment_date}")
