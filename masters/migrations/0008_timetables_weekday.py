# Generated by Django 2.2.28 on 2024-01-09 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0007_auto_20240109_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetables',
            name='weekday',
            field=models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='Tuesday', max_length=10),
        ),
    ]