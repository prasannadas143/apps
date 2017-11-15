from appointmentscheduler.models import AppschedulerEmployees
from django import forms

class ReportForm(forms.ModelForm):
    class Meta:
        model = AppschedulerEmployees
        fields = '__all__'

