# Generated by Django 4.2.5 on 2024-01-16 16:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0023_divegroup_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divegroup',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Dive Date'),
        ),
    ]
