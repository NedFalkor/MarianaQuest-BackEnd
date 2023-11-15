from django.db import models
from rest_framework.exceptions import ValidationError
from MQ_users.models import CustomUser


class DiveGroup(models.Model):
    group_number = models.IntegerField(unique=True, verbose_name="Group Number")
    boat_driver = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="led_dive_groups_as_driver",
        verbose_name="Boat Driver",
        limit_choices_to={'role': 'FORMATEUR'},
        null=True
    )
    trainer_one = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="led_dive_groups_as_trainer_one",
        verbose_name="First Trainer",
        limit_choices_to={'role': 'FORMATEUR'},
        null=True
    )
    trainer_two = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="led_dive_groups_as_trainer_two",
        verbose_name="Second Trainer",
        limit_choices_to={'role': 'FORMATEUR'},
        null=True
    )
    divers = models.ManyToManyField(
        CustomUser,
        related_name="dive_groups",
        verbose_name="Divers",
        limit_choices_to={'role': 'PLONGEUR'}
    )
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    def __str__(self):
        boat_driver_username = getattr(self.boat_driver, 'username', 'No driver')
        return f"Group {self.group_number} led by {boat_driver_username}"

    def clean(self):
        # Ensure the boat driver is present and is a trainer
        if not self.boat_driver or getattr(self.boat_driver, 'role', None) != 'FORMATEUR':
            raise ValidationError("Un conducteur de bateau formateur est requis.")

        # Validate that each trainer has between 1 and 2 divers
        trainer_with_diver_present = False
        for trainer in [self.trainer_one, self.trainer_two]:
            if trainer:
                diver_count = self.divers.filter(role='PLONGEUR').count()
                if diver_count < 1 or diver_count > 2:
                    raise ValidationError(f"{getattr(trainer, 'username', None)} doit avoir entre 1 et 2 plongeurs.")
                trainer_with_diver_present = True

        if not trainer_with_diver_present:
            raise ValidationError("Au moins un formateur avec un plongeur est requis.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
