# Generated by Django 5.1.1 on 2024-10-16 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0011_remove_user_profile_picture"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Admin",
        ),
        migrations.DeleteModel(
            name="Karyawan",
        ),
    ]
