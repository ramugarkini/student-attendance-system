# Generated by Django 2.2.28 on 2024-01-11 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0019_auto_20240111_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentyears',
            name='current_academic_year',
            field=models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year'), ('G', 'Graduated')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='academic_year',
            field=models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')], default='1st Year', max_length=1),
        ),
        migrations.AlterField(
            model_name='timetables',
            name='weekday',
            field=models.CharField(choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday')], default='Thursday', max_length=1),
        ),
    ]