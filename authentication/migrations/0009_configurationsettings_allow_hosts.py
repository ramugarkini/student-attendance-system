# Generated by Django 4.2.9 on 2024-01-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20240111_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurationsettings',
            name='allow_hosts',
            field=models.BooleanField(default=True),
        ),
    ]