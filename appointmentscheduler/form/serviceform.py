from django import forms
from appointmentscheduler.models import  AppschedulerServices

class ServiceForm(forms.ModelForm):
    class Meta:
        model = AppschedulerServices
        fields = '__all__'
