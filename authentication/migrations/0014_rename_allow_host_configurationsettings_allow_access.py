# Generated by Django 4.2.9 on 2024-01-17 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_rename_user_name_configurationsettings_server_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationsettings',
            old_name='allow_host',
            new_name='allow_access',
        ),
    ]
