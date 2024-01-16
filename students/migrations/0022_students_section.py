# Generated by Django 2.2.28 on 2024-01-11 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0023_auto_20240111_2027'),
        ('students', '0021_auto_20240110_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='masters.Sections'),
            preserve_default=False,
        ),
    ]