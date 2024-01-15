from django.db import models
from MQ_users.models import CustomUser


class DiveGroup(models.Model):
    group_description = models.CharField(max_length=255, verbose_name="Group Description", null=True, blank=True)
    boat_driver = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="led_dive_groups_as_driver",
        verbose_name="Boat Driver",
        limit_choices_to={'role': 'INSTRUCTOR'},
        null=True
    )
    trainer_one = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="led_dive_groups_as_trainer_one",
        verbose_name="First Trainer",
        limit_choices_to={'role': 'INSTRUCTOR'},
        null=True
    )
    trainer_two = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="led_dive_groups_as_trainer_two",
        verbose_name="Second Trainer",
        limit_choices_to={'role': 'INSTRUCTOR'},
        null=True
    )
    divers = models.ManyToManyField(
        CustomUser,
        related_name="dive_groups",
        verbose_name="Divers",
        limit_choices_to={'role': 'DIVER'}
    )
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    def __str__(self):
        # Updated to use group_description instead of group_number
        return f"{self.group_description}"

    def get_divers_list(self):
        # This method can stay as is, it correctly lists diver usernames.
        return ", ".join([diver.username for diver in self.divers.all()])

