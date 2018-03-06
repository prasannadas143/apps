from django.db import models

# Create your models here.
class ShippingAndTax(models.Model):
	location = models.CharField(max_length=100, unique=True, blank=False, null=False )
	shipping = models.DecimalField(max_digits=9, decimal_places=2, default=0)
	free_shipping = models.DecimalField(max_digits=9, decimal_places=2, default=0)
	tax = models.DecimalField(max_digits=9, decimal_places=2, default=0)

	class Meta:
		# managed = False
		db_table = 'shoppingcart_shippingandtax'
		ordering = ['-id']
