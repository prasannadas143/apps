from django.db import models

# Create your models here.
class Products(models.Model):
    PRIORITY_CHOICES = ((True, 'active'),
                        (False, 'inactive'),)
    product_name = models.CharField(max_length=255, unique=True, blank=False, null=False )
    product_desc = models.TextField(blank=False, null=False)
    product_img = models.ImageField(upload_to = product_img_location, default = 'product/no-img.jpg')
    product_price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    product_id = models.SmallIntegerField( blank=False, null=False, default= 0)
    
    product_status = models.BooleanField(choices=PRIORITY_CHOICES,  default=True)
    emp_service = models.ManyToManyField(AppschedulerEmployees,  blank=True)
    is_featured = models.BooleanField(default=False )

    class Meta:
        # managed = False
        db_table = 'shoppingcart_products'
		ordering = ['-id']

    
	def __str__(self):
		return self.product_name
		
	def get_absolute_url(self):
		return reverse('shoppingcart_detail', args=(self.slug,))	

    def get_success_url(self):
        return reverse('shoppingcart-list')

