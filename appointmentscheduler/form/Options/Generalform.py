from appointmentscheduler.models import AppschedulerOptions
from django import forms

class OptionsForm(forms.ModelForm):
    class Meta:
        model = AppschedulerOptions
        fields = '__all__'