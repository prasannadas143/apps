from django import forms
from .models import  SmsEmailTemplates, SmsEmailTemplatesDetails


class FormTemplate(forms.ModelForm):
    class Meta:
        model = SmsEmailTemplates
        fields = '__all__'


class FormTemplateDetails(forms.ModelForm):
    class Meta:
        model = SmsEmailTemplatesDetails
        fields = '__all__'