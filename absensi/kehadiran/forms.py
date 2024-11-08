from django import forms
from .models import Kehadiran

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Kehadiran
        fields = []