from django.shortcuts import redirect
from django.urls import reverse

class KaryawanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/karyawan/'):
            if not request.user.is_authenticated or not request.user.groups.filter(name='Karyawan').exists():
                return redirect(reverse('admin_home'))

        response = self.get_response(request)
        return response