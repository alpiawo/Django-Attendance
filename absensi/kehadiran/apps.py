from django.apps import AppConfig


class KehadiranConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kehadiran"

    def ready(self):
        from .views import update_attendance_status
        update_attendance_status()