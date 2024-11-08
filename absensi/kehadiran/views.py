from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Kehadiran, Announcement
from django.utils import timezone
from datetime import datetime, time as datetime_time
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import timedelta
from user.models import User


def update_attendance_status():
    # Get waktu saat ini
    now = timezone.localtime()

    # Ambil semua pengguna dengan role Karyawan
    karyawan_users = User.objects.filter(role=User.Role.KARYAWAN)

    if now.time() >= datetime_time(10, 0):
        for user in karyawan_users:
            start_date = max(user.date_joined.date(), now.date() - timedelta(days=7))
            attendance_dates = pd.date_range(start=start_date, end=now.date()).date

            for date in attendance_dates:
                attendance, created = Kehadiran.objects.get_or_create(user=user, date=date)

                if not attendance.check_in_time and attendance.status not in ['Izin', 'Izin Telat']:
                    attendance.status = 'Alpha'
                    attendance.save()


@login_required
def check_in(request):
    update_attendance_status()  # Memanggil fungsi untuk memperbarui status kehadiran
    today = timezone.localtime().date()
    attendance, created = Kehadiran.objects.get_or_create(user=request.user, date=today)

    # jika user tanpa status sampai jam 10 am = alpha
    now = timezone.localtime()
    if now.time() >= datetime_time(0, 00) and not attendance.check_in_time and attendance.status not in ['Izin', 'Izin Telat']:
        attendance.status = 'Alpha'
        attendance.save()
        return render(request, 'attendance/message.html', {'message': "Anda telah ditandai sebagai Alpha karena belum absensi."})

    # Jika user memiliki status izin
    if attendance.status == 'Izin':
        message = "Anda sedang izin dan tidak dapat melakukan check-in."
        return render(request, 'attendance/izin.html', {'message': message})

    # Jika user sudah check-in
    if attendance.check_in_time:
        allowed_checkout_time = datetime_time(0, 30)
        now_time = now.time()
        if now_time >= allowed_checkout_time:
            return redirect('kehadiran:check_out')

    # Proses check-in
    if request.method == 'POST':
        izin_option = request.POST.get('izin_option')
        alasan = request.POST.get('alasan_izin', '')  # Ambil alasan dari form jika ada
        durasi_izin = int(request.POST.get('durasi_izin', 0))  # Ambil durasi izin

        if izin_option == 'izin_telat':
            attendance.status = 'Izin Telat'
            attendance.save()
            return redirect('kehadiran:konfirmasi_telat')

        elif izin_option == 'izin':  # Jika izin dipilih
            if alasan and durasi_izin > 0:  # Pastikan alasan dan durasi diisi
                # Tandai izin untuk rentang hari yang diajukan
                for i in range(durasi_izin):
                    izin_date = today + timedelta(days=i)
                    izin_attendance, created = Kehadiran.objects.get_or_create(user=request.user, date=izin_date)
                    izin_attendance.status = 'Izin'
                    izin_attendance.alasan_izin = alasan
                    izin_attendance.durasi_izin = durasi_izin
                    izin_attendance.save()

                return redirect('kehadiran:attendance_summary')
            else:
                # Tampilkan error jika alasan atau durasi izin tidak diisi
                return render(request, 'attendance/check_in.html', {
                    'attendance': attendance,
                    'error': "Alasan izin dan durasi izin harus diisi!"
                })

        # Proses check-in
        now = timezone.localtime().time()
        attendance.mark_attendance(check_in=now)
        return redirect('kehadiran:attendance_summary')

    return render(request, 'attendance/check_in.html', {'attendance': attendance})


@login_required
def konfirmasi_telat(request):
    today = timezone.localtime().date()
    attendance = Kehadiran.objects.get(user=request.user, date=today)

    if request.method == 'POST':
        # Ambil waktu check-in dari input form
        check_in_time_str = request.POST.get('check_in_time')
        # Mengonversi string menjadi waktu
        check_in_time = datetime.strptime(check_in_time_str, '%H:%M').time()

        # Tandai kehadiran
        attendance.check_in_time = check_in_time

        # Pastikan status tetap "Izin Telat"
        attendance.status = 'Izin Telat'
        attendance.save()

        return redirect('kehadiran:attendance_summary')

    return render(request, 'attendance/konfirmasi_telat.html', {'attendance': attendance})


@login_required
def check_out(request):
    today = timezone.localtime().date()
    attendance = Kehadiran.objects.get(user=request.user, date=today)

    # Cek jika pengguna memiliki status izin
    if attendance.status == 'Izin':
        message = "Anda sedang izin, terimakasih😊."
        return render(request, 'attendance/izin.html', {'message': message})

    # Pastikan user sudah check-in sebelum check-out
    if attendance.check_in_time is None:
        return redirect('attendance_summary')

    if attendance.check_in_time and attendance.check_out_time:
        message = f"Anda sudah check-in pada {attendance.check_in_time.strftime('%H:%M:%S')} dan check-out pada {attendance.check_out_time.strftime('%H:%M:%S')} dengan status '{attendance.status}'."
        return render(request, 'attendance/summary.html', {'message': message, 'attendance': attendance})

    # Cek apakah sudah melewati waktu check-out yang diizinkan
    now = timezone.localtime().time()
    allowed_checkout_time = datetime_time(0, 30)

    if now < allowed_checkout_time:
        return render(request, 'attendance/check_out.html', {'attendance': attendance})

    if request.method == 'POST':
        now = timezone.localtime().time()
        attendance.mark_attendance(check_out=now)
        return redirect('kehadiran:attendance_summary')

    return render(request, 'attendance/check_out.html', {'attendance': attendance})


@login_required
def export(request):
    kehadiran = Kehadiran.objects.select_related('user').all()

    data = []

    for record in kehadiran:
        nama_lengkap = f"{record.user.first_name} {record.user.last_name}"
        data.append({
            'Nama Pengguna': nama_lengkap,
            'Email': record.user.email,
            'Tanggal': record.date.strftime('%d-%m-%Y'),
            'Check In': record.check_in_time.strftime('%H:%M:%S') if record.check_in_time else 'N/A',
            'Check Out': record.check_out_time.strftime('%H:%M:%S') if record.check_out_time else 'N/A',
            'Status': record.status,
        })

    df = pd.DataFrame(data)

    # Menentukan response untuk file Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data-kehadiran.xlsx'

    df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required
def attendance_summary(request):
    attendances = Kehadiran.objects.filter(user=request.user).order_by('-date')
    return render(request, 'attendance/attendance_summary.html', {'attendances': attendances})

@login_required
def announcement_karyawan(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'attendance/announcement.html', {'announcements': announcements})

@login_required
def dashboard(request):
    return render(request, 'home.html')


def is_admin(user):
    return user.is_staff