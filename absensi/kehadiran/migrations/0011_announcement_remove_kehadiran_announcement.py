# Generated by Django 5.1.1 on 2024-10-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kehadiran", "0010_kehadiran_announcement"),
    ]

    operations = [
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="kehadiran",
            name="announcement",
        ),
    ]
