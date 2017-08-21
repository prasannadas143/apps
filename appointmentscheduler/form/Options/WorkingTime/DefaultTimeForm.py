from appointmentscheduler.models import AppschedulerDates
from django import forms


class customtimeform(forms.ModelForm):
    class Meta:
        model = AppschedulerDates
        fields = ['date', 'start_time', 'end_time', 'start_launch', 'end_launch', 'is_dayoff']
