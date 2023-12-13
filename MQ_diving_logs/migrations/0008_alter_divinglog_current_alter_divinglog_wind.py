# Generated by Django 4.2.5 on 2023-12-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_diving_logs', '0007_alter_divinglog_current_alter_divinglog_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divinglog',
            name='current',
            field=models.CharField(blank=True, choices=[('none', 'None'), ('weak', 'Weak'), ('medium', 'Medium'), ('strong', 'Strong')], max_length=10, verbose_name='Current'),
        ),
        migrations.AlterField(
            model_name='divinglog',
            name='wind',
            field=models.CharField(blank=True, choices=[('none', 'None'), ('weak', 'Weak'), ('medium', 'Medium'), ('strong', 'Strong')], max_length=10, verbose_name='Wind'),
        ),
    ]
