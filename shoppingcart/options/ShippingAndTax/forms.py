from django import forms
from .models import  ShippingAndTax

class ShippingAndTaxForm(forms.ModelForm):

	class Meta:
	    model = ShippingAndTax
	    fields = '__all__'