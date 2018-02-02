from django import forms


from shoppingcart.clients.models import  Clients, Addresses
from django import forms

class ClientsForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
	    model = Clients
	    fields = '__all__'

class AddressesForm(forms.ModelForm):
    class Meta:
        model = Addresses
        exclude = ('country','client','created','last_login')
