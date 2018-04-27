from django import forms
from ..models import  Attributes

class AttributesForm(forms.ModelForm):

	class Meta:
	    model = Attributes
	    fields = '__all__'