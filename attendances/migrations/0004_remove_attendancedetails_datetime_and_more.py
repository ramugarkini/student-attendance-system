# Generated by Django 4.2.9 on 2024-01-12 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0003_remove_attendances_timetable_detail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancedetails',
            name='datetime',
        ),
        migrations.AddField(
            model_name='attendancedetails',
            name='in_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='attendancedetails',
            name='out_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='attendances',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='attendances',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
