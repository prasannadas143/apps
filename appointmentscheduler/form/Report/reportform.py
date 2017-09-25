from appointmentscheduler.models import AppschedulerEmployees
from django import forms
from appointmentscheduler.models import  AppschedulerServices

class ReportForm(forms.ModelForm):
    class Meta:
        model = AppschedulerEmployees
        fields = '__all__'

