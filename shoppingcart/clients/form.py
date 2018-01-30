from django import forms


from shoppingcart.clients.models import  Clients, Addresses

class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'

class AddressesForm(forms.ModelForm):
    class Meta:
        model = Addresses
        exclude = ('country','client')
