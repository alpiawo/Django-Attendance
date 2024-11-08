from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, time


class Kehadiran(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    is_present = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('Telat', 'Telat'),
        ('Tidak Telat', 'Tidak Telat'),
        ('Izin', 'Izin'),
        ('Izin Telat', 'Izin Telat'),
        ('Alpha', 'Alpha'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Tidak Telat')
    alasan_izin = models.TextField(null=True, blank=True)
    durasi_izin = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.status == 'Izin':
            return f"Absensi {self.user} sedang {self.status} dengan alasan: {self.alasan_izin}, selama {self.durasi_izin} hari"
        else:
            return f"Absensi Hadir {self.user}. Tanggal {self.date} Jam: {self.check_in_time}, ({self.status}). Check Out: {self.check_out_time}"

    def mark_attendance(self, check_in=None, check_out=None, izin=False, alasan=None, durasi=None):
        if izin:
            self.status = 'Izin'
            self.is_present = False
            self.check_in_time = None
            self.check_out_time = None
            self.alasan_izin = alasan
            self.durasi_izin = durasi
        else:
            if check_in:
                self.check_in_time = check_in
                self.is_present = True

                # Menentukan Status Kehadiran
                late_time = datetime.combine(self.date, time(8, 00))
                self.status = 'Telat' if check_in >= late_time.time() else 'Tidak Telat'

            if check_out:
                self.check_out_time = check_out

        self.save()

    def save(self, *args, **kwargs):
        if self.check_out_time and not self.check_in_time:
            raise ValidationError("Check-out time tidak dapat diatur tanpa check-in time.")

        super().save(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

