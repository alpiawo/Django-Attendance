# Generated by Django 5.1.1 on 2024-10-06 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_user_profile_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="profile_picture",
        ),
    ]