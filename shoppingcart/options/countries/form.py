from django import forms

from shoppingcart.options.countries.models import  Countries

class CountriesForm(forms.ModelForm):
    class Meta:
        model = Countries
        fields = '__all__'