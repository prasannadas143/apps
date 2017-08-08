from appointmentscheduler.models import AppschedulerDates
from django import forms


class customtimeform(forms.ModelForm):
    class Meta:
        model = AppschedulerDates
        fields = '__all__'
