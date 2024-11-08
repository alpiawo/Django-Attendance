from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import User
from kehadiran.models import Announcement
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Announcement)