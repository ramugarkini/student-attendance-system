# Generated by Django 4.2.9 on 2024-01-13 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0030_alter_timetables_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetables',
            name='weekday',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1),
        ),
    ]
