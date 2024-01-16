# Generated by Django 2.2.28 on 2024-01-11 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0021_auto_20240111_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetabledetails',
            name='subject',
        ),
        migrations.AddField(
            model_name='timetabledetails',
            name='subject_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masters.SubjectDetails'),
        ),
    ]