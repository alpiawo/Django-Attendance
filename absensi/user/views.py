from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import   login_required
from .forms import UserRegistrationForm, UserLoginForm
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .forms import AnnouncementForm
from kehadiran.models import Kehadiran, Announcement
from .models import User
import random
import pytz
import hashlib
from datetime import datetime


# Create your views here.

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registrasi user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login user
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Generate OTP
                otp = random.randint(100000, 999999)

                # Simpan OTP ke sesi pengguna
                request.session['otp'] = otp
                request.session['username'] = user.username

                # Kirim email dengan OTP
                send_mail(
                    'Kode OTP Anda',
                    f'Kode OTP Anda adalah {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                # Redirect ke halaman verifikasi OTP
                return redirect('user:verify_otp')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Username atau password salah'})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# Verifikasi OTP
def verify_otp(request):
    if request.method == 'POST':
        # Mengambil semua bagian dari OTP
        input_otp = (
            request.POST.get('otp1') +
            request.POST.get('otp2') +
            request.POST.get('otp3') +
            request.POST.get('otp4') +
            request.POST.get('otp5') +
            request.POST.get('otp6')
        )
        session_otp = request.session.get('otp')
        username = request.session.get('username')

        if input_otp == str(session_otp):
            # Login user setelah OTP valid
            user = User.objects.get(username=username)
            login(request, user)

            # Redirect sesuai role user
            if user.role == User.Role.KARYAWAN:
                return redirect('user:karyawan_home')
            elif user.role == User.Role.ADMIN:
                return redirect('user:admin_home')
        else:
            return render(request, 'verifikasi.html', {'error': 'Invalid OTP'})

    return render(request, 'verifikasi.html')


def user_logout(request):
    logout(request)
    return redirect('user:login')

def home(request):
    return render(request, 'home.html')

# Halaman home untuk karyawan (dibatasi oleh middleware)
@login_required
def karyawan_home(request):
    user = request.user
    if user.role != User.Role.KARYAWAN:
        return HttpResponseForbidden("Unauthorized", status=403)

    announcements = Announcement.objects.all().order_by('-created_at')[:3]
    total_telat = Kehadiran.objects.filter(user=user, status='Telat').count()
    total_tidak_telat = Kehadiran.objects.filter(user=user,status='Tidak Telat').count()
    total_alpha = Kehadiran.objects.filter(user=user, status='Alpha').count()

    context = {
        'total_telat': total_telat,
        'total_tidak_telat': total_tidak_telat,
        'total_alpha': total_alpha,
        'announcements': announcements
    }

    return render(request, 'karyawan/home.html', context)

@login_required
def get_user_tidak_telat(request):
    user = request.user
    if user.role != User.Role.KARYAWAN:
        return HttpResponseForbidden("You are not authorized to view this admin.")
    tidak_telat_records = Kehadiran.objects.filter(user=user, status='Tidak Telat')

    events = []
    for record in tidak_telat_records:
        events.append({
            'title': 'Hadir',
            'start': record.date.isoformat(),  # Tanggal kehadiran
            'backgroundColor': 'green',  # Warna untuk event hadir
            'borderColor': 'green',
            'textColor': 'white',
        })

    return JsonResponse(events, safe=False)

@login_required
def get_user_telat(request):
    user = request.user
    if user.role != User.Role.KARYAWAN:
        return HttpResponseForbidden("You are not authorized to view this admin.")
    telat_records = Kehadiran.objects.filter(user=user, status='Telat')

    events = []
    for record in telat_records:
        events.append({
            'title': 'Telat',
            'start': record.date.isoformat(),
            'backgroundColor': 'yellow',
            'borderColor': 'yellow',
            'textColor': 'black',
            'event': 'telat',
        })

    return JsonResponse(events, safe=False)

@login_required
def get_user_izin(request):
    user = request.user
    if user.role != User.Role.KARYAWAN:
        return HttpResponseForbidden("You are not authorized to view this admin.")
    izin_records = Kehadiran.objects.filter(user=user, status='Izin')

    events = []
    for record in izin_records:
        events.append({
            'title': 'Izin',
            'start': record.date.isoformat(),
            'backgroundColor': 'blue',
            'borderColor': 'blue',
            'textColor': 'white',
            'event': 'izin',
        })

    return JsonResponse(events, safe=False)

@login_required
def get_user_alpha(request):
    user = request.user
    if user.role != User.Role.KARYAWAN:
        return HttpResponseForbidden("You are not authorized to view this admin.")
    alpha_records = Kehadiran.objects.filter(user=user, status='Alpha')

    events = []
    for record in alpha_records:
        events.append({
            'title': 'Alpha',
            'start': record.date.isoformat(),
            'backgroundColor': 'red',
            'borderColor': 'red',
            'textColor': 'white',
            'event': 'alpha',
        })

    return JsonResponse(events, safe=False)


@login_required
def admin_home(request):
    user = request.user
    if user.role != User.Role.ADMIN:
        return HttpResponseForbidden("You are not authorized to view this admin page.")

    # Get all users with the role of KARYAWAN
    karyawan_users = User.objects.filter(role=User.Role.KARYAWAN)

    # Current month
    current_month = datetime.now().month

    # Initialize statistics
    total_karyawan = karyawan_users.count()
    present_count = 0
    izin_count = 0
    alpha_count = 0

    # Loop through users and calculate attendance stats for the current month
    for karyawan in karyawan_users:
        attendances = Kehadiran.objects.filter(user=karyawan, date__month=current_month)

        # Count present, izin (late leave), and alpha (absent without notice) for this month
        present_count += attendances.filter(status='present').count()
        izin_count += attendances.filter(status='izin').count()
        alpha_count += attendances.filter(status='alpha').count()

    # Pass the data to the template
    context = {
        'karyawan_users': karyawan_users,
        'total_karyawan': total_karyawan,
        'present_count': present_count,
        'izin_count': izin_count,
        'alpha_count': alpha_count,
    }

    return render(request, 'admin/home.html', context)

@login_required
def admin_attendance_check(request):
    user = request.user
    if user.role != User.Role.ADMIN:
        return HttpResponseForbidden("You are not authorized to view this admin.")

    # Mengatur timezone ke Asia/Jakarta
    jakarta_tz = pytz.timezone('Asia/Jakarta')

    # Mengambil waktu saat ini dalam zona waktu Jakarta
    now_jakarta = timezone.now().astimezone(jakarta_tz)
    today = now_jakarta.date()  # Mengambil tanggal saat ini
    search_query = request.GET.get('q')

    if search_query:
        attendances = Kehadiran.objects.exclude(user__is_staff=True).filter(date=today,user__username__icontains=search_query)
    else:
        attendances = Kehadiran.objects.exclude(user__is_staff=True).filter(date=today)
    return render(request, 'admin/attendance-user.html', {'attendances': attendances})

@login_required
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'admin/announcement_list.html'
    context_object_name = 'announcements'

@login_required
def announcement_view(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'admin/announcement_list.html', {'announcements': announcements})

@login_required
@csrf_exempt
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
@csrf_exempt
def update_announcement(request):
    if request.method == 'POST':
        announcement_id = request.POST.get('id')
        announcement = Announcement.objects.get(id=announcement_id)
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
@csrf_exempt
def delete_announcement(request):
    if request.method == 'POST':
        announcement_id = request.POST.get('id')
        announcement = Announcement.objects.get(id=announcement_id)
        announcement.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def admin_profile(request):
    user = request.user
    if user.role != User.Role.ADMIN:
        return HttpResponseForbidden("You are not authorized to view this admin.")

    return render(request, 'admin/profile.html')

#profile karyawan
@login_required
def karyawan_profile(request):
    user = request.user
    if user.role != User.Role.KARYAWAN:
        return HttpResponseForbidden("You are not authorized to view this admin.")

    recent_absensi = Kehadiran.objects.filter(user=user).order_by('-date')[:3]
    context = {
        'recent_absensi': recent_absensi,
    }

    return render(request, 'karyawan/profile.html', context)