# Generated by Django 4.2.9 on 2024-01-17 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_configurationsettings_client_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationsettings',
            old_name='user_name',
            new_name='server_user_name',
        ),
    ]
