# Generated by Django 4.2.5 on 2023-12-20 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0019_alter_emergencycontact_diver_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='diver_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contacts', to='MQ_users.diverprofile'),
        ),
    ]
