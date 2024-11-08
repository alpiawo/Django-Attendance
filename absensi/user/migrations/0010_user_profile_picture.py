# Generated by Django 5.1.1 on 2024-10-06 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0009_remove_user_profile_pic"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(default="default.jpg", upload_to="profile_pics/"),
        ),
    ]
