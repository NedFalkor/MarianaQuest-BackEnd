# Generated by Django 4.2.5 on 2024-01-15 10:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0022_remove_divegroup_group_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='divegroup',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Some Date'),
        ),
    ]