from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
from shoppingcart.options.countries.models import Countries
# Create your models here.

class Clients(models.Model):
    email = models.EmailField(unique=True,  validators=[validators.validate_email,])
    password = models.CharField(max_length=50)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    phone = PhoneNumberField(unique=True,  blank=False, null=False)
    website = models.URLField(blank=True, null=True)
    created = models.DateTimeField(blank=False, null=False)
    last_login = models.DateTimeField(blank=False, null=False)
    status =  models.BooleanField(default=False)
    # order = models.ForeignKey(
    #         'Order',
    #         on_delete=models.CASCADE,
    #        related_name="order_client", related_query_name="order_client" , blank=True,null=True
    # )    
    def __str__(self):
        return self.client_name

    def get_absolute_url(self):
        return '/shoppingcart/clients/editClient/' + self.id + '/'


    def get_success_url(self):
        return '/shoppingcart/clients/listClients/'

    class Meta:
        db_table = 'shoppingcart_clients'
        ordering = ['-id']
        unique_together = (('email'),)



class Addresses(models.Model):
    country = models.ForeignKey(
        Countries,
        on_delete=models.CASCADE,
        related_name="address_country",  related_query_name="address_country",blank=True,null=True
        
        
    ) 
    state = models.CharField(max_length=255,blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    client_zip = models.CharField(max_length=255,blank=False, null=False)
    address_1 = models.CharField(max_length=2000,blank=False, null=False)
    address_2 = models.CharField(max_length=2000, blank=True, null=True)
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing =  models.BooleanField(default=False)
    client = models.ForeignKey(
        'Clients',
        on_delete=models.CASCADE,
       related_name="address_client", related_query_name="address_client" , blank=True,null=True
    )    

    class Meta:
        db_table = 'shoppingcart_addresses'
        ordering = ['-id']

    def __str__(self):
        return self.client.client_name

