from django import forms

from appointmentscheduler.models import  AppschedulerTemplates

class addTemplate(forms.ModelForm):
    class Meta:
        model = AppschedulerTemplates
        fields = '__all__'