from appointmentscheduler.models import AppschedulerCountries
from django import forms

from appointmentscheduler.models import  AppschedulerCountries

class Countries(forms.ModelForm):
    class Meta:
        model = AppschedulerCountries
        fields = '__all__'