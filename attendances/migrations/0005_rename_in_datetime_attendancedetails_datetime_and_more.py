# Generated by Django 4.2.9 on 2024-01-12 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0004_remove_attendancedetails_datetime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancedetails',
            old_name='in_datetime',
            new_name='datetime',
        ),
        migrations.RemoveField(
            model_name='attendancedetails',
            name='out_datetime',
        ),
    ]