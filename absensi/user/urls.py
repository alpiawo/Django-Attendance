from django.urls import path
from .views import karyawan_home, admin_home, user_login, user_logout, register, home, karyawan_profile, verify_otp, get_user_tidak_telat, get_user_telat, get_user_alpha, get_user_izin, admin_attendance_check, admin_profile, announcement_view, create_announcement, update_announcement, delete_announcement

app_name = 'user'

urlpatterns = [
    path('', home, name='home' ),
    path('login/', user_login, name='login'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('karyawan/home/', karyawan_home, name='karyawan_home'),
    path('karyawan/profile/', karyawan_profile, name='karyawan_profile'),
    path('get_user_tidak_telat/', get_user_tidak_telat, name='get_user_tidak_telat'),
    path('get_user_telat/', get_user_telat, name='get_user_telat'),
    path('get_user_alpha/', get_user_alpha, name='get_user_alpha'),
    path('get_user_izin/', get_user_izin, name='get_user_izin'),
    path('administrator/home/', admin_home, name='admin_home'),
    path('administrator/profile/', admin_profile, name='admin_profile'),
    path('administrator/check-attendance', admin_attendance_check, name='admin_attendance_check'),
    path('administrator/announcements/', announcement_view, name='announcement_view'),
    path('administrator/announcements/create/', create_announcement, name='announcement_create'),
    path('administrator/announcements/update/', update_announcement, name='announcement_update'),
    path('administrator/announcements/delete/', delete_announcement, name='announcement_delete'),
]