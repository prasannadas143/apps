from appointmentscheduler.models import AppschedulerBookings
from django import forms


class BookingForm(forms.ModelForm):
    class Meta:
        model = AppschedulerBookings
        fields = '__all__'



