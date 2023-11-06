# Generated by Django 4.2.5 on 2023-11-05 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0006_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiveGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.IntegerField(unique=True, verbose_name='Group Number')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='led_dive_groups', to=settings.AUTH_USER_MODEL, verbose_name='Group Leader')),
                ('members', models.ManyToManyField(related_name='dive_groups', to=settings.AUTH_USER_MODEL, verbose_name='Group Members')),
            ],
        ),
    ]