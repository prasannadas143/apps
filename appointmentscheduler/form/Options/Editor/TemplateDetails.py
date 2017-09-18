from appointmentscheduler.models import AppschedulerTemplatesDetails
from django import forms

from appointmentscheduler.models import  AppschedulerTemplatesDetails

class TemplateDetails(forms.ModelForm):
    class Meta:
        model = AppschedulerTemplatesDetails
        fields = '__all__'