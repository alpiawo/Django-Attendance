# Generated by Django 5.1.1 on 2024-10-06 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0008_user_profile_pic"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="profile_pic",
        ),
    ]