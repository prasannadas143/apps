from appointmentscheduler.models import AppschedulerEmployees
from django import forms

from appointmentscheduler.models import  AppschedulerServices

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,error_messages={'required': 'Please enter password!'})
    class Meta:
        model = AppschedulerEmployees
        fields = '__all__'



