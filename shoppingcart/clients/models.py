# from django.db import models

# # Create your models here.

# class Clients(models.Model):
#     email = models.EmailField(unique=True,  validators=[validators.validate_email,])
#     password = models.TextField(blank=True, null=True)
#     client_name = models.CharField(max_length=255, blank=True, null=True)
#     phone = PhoneNumberField(unique=True,  blank=False, null=False)

#     url = models.CharField(max_length=255, blank=True, null=True)
#     created = models.DateTimeField(blank=True, null=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(max_length=1)
# 	# order = models.ForeignKey(
# 	#         'Order',
# 	#         on_delete=models.CASCADE,
# 	#        related_name="order_client", related_query_name="order_client" , blank=True,null=True
# 	# )    

#     class Meta:
#         db_table = 'shopping_cart_clients'

# class Addresses(models.Model):
#     client_id = models.IntegerField(blank=True, null=True)
#     country_id = models.IntegerField(blank=True, null=True)
#     state = models.CharField(max_length=255, blank=True, null=True)
#     city = models.CharField(max_length=255, blank=True, null=True)
#     client_zip = models.CharField(max_length=255, blank=True, null=True)
#     address_1 = models.CharField(max_length=255, blank=True, null=True)
#     address_2 = models.CharField(max_length=255, blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     is_default_shipping = models.IntegerField(blank=True, null=True)
#     is_default_billing = models.IntegerField(blank=True, null=True)
#     client = models.ForeignKey(
#         'Clients',
#         on_delete=models.CASCADE,
#        related_name="client_addresses", related_query_name="client_addresses" , blank=True,null=True
#     )    

#     class Meta:
#         db_table = 'shopping_cart_addresses'
