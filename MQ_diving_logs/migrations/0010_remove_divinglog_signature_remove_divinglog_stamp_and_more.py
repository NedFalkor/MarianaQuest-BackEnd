# Generated by Django 4.2.5 on 2023-12-21 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MQ_diving_logs', '0009_divinglog_dive_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='divinglog',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='divinglog',
            name='stamp',
        ),
        migrations.AddField(
            model_name='instructorcomment',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/', verbose_name='Signature'),
        ),
        migrations.AddField(
            model_name='instructorcomment',
            name='stamp',
            field=models.ImageField(blank=True, null=True, upload_to='stamps/', verbose_name='Stamp'),
        ),
        migrations.AlterField(
            model_name='divinglog',
            name='status',
            field=models.CharField(choices=[('AWAITING', 'Awaiting'), ('VALIDATED', 'Validated'), ('REFUSED', 'Refused')], default='VALIDATED', max_length=10),
        ),
    ]