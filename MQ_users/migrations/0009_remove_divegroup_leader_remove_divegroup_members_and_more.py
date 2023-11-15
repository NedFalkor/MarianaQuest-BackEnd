# Generated by Django 4.2.5 on 2023-11-15 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0008_alter_customuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='divegroup',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='divegroup',
            name='members',
        ),
        migrations.AddField(
            model_name='divegroup',
            name='boat_driver',
            field=models.ForeignKey(limit_choices_to={'role': 'FORMATEUR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_dive_groups_as_driver', to=settings.AUTH_USER_MODEL, verbose_name='Boat Driver'),
        ),
        migrations.AddField(
            model_name='divegroup',
            name='divers',
            field=models.ManyToManyField(limit_choices_to={'role': 'PLONGEUR'}, related_name='dive_groups', to=settings.AUTH_USER_MODEL, verbose_name='Divers'),
        ),
        migrations.AddField(
            model_name='divegroup',
            name='trainer_one',
            field=models.ForeignKey(limit_choices_to={'role': 'FORMATEUR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_dive_groups_as_trainer_one', to=settings.AUTH_USER_MODEL, verbose_name='First Trainer'),
        ),
        migrations.AddField(
            model_name='divegroup',
            name='trainer_two',
            field=models.ForeignKey(limit_choices_to={'role': 'FORMATEUR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_dive_groups_as_trainer_two', to=settings.AUTH_USER_MODEL, verbose_name='Second Trainer'),
        ),
    ]