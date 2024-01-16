# Generated by Django 2.2.28 on 2024-01-09 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0008_timetables_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetables',
            name='weekday',
            field=models.CharField(choices=[('1', 'Sunday'), ('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday')], default='Tuesday', max_length=10),
        ),
    ]