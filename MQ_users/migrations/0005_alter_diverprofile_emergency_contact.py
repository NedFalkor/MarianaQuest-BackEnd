# Generated by Django 4.2.5 on 2023-10-31 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0004_emergencycontact_diverprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diverprofile',
            name='emergency_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MQ_users.emergencycontact'),
        ),
    ]
