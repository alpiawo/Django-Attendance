from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# from django.db.models.expressions import result


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "Admin", 'Admin'
        KARYAWAN = "Karyawan", 'Karyawan'

    base_role = Role.KARYAWAN

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.KARYAWAN)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            self.is_staff = self.role == self.Role.ADMIN
            return super().save(*args, **kwargs)
