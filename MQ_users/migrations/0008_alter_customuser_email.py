# Generated by Django 4.2.5 on 2023-11-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_users', '0007_divegroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
