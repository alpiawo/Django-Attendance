from django.urls import path
from .views import export, check_in, check_out, konfirmasi_telat, attendance_summary, announcement_karyawan

app_name = 'kehadiran'

urlpatterns = [
    path('export/', export, name='export'),
    path('karyawan/check-in/', check_in, name='check_in'),
    path('karyawan/check-out/', check_out, name='check_out'),
    path('karyawan/lated-confirmation/', konfirmasi_telat, name='konfirmasi_telat'),
    path('karyawan/history-summary/', attendance_summary, name='attendance_summary'),
    path('karyawan/announcement/', announcement_karyawan, name='announcement_karyawan'),
]