# Generated by Django 5.1.1 on 2024-09-25 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kehadiran", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="kehadiran",
            name="is_present",
            field=models.BooleanField(default=False),
        ),
    ]
