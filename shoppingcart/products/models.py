# from django.db import models

# # Create your models here.

# class Products(models.Model):
# 	PRIORITY_CHOICES = ((True, 'active'),
# 	                    (False, 'inactive'),)
# 	product_name = models.CharField(max_length=255, unique=True, blank=False, null=False )
# 	product_desc = models.TextField(blank=False, null=False)
# 	product_img = models.ImageField(upload_to = 'product', default = 'product/no-img.jpg')
# 	product_price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
# 	product_id = models.SmallIntegerField( blank=False, null=False, default= 0)

# 	product_status = models.BooleanField(choices=PRIORITY_CHOICES,  default=True)
# 	# emp_service = models.ManyToManyField(AppschedulerEmployees,  blank=True)
# 	is_featured = models.BooleanField(default=False )

# 	class Meta:
# 		db_table = 'shoppingcart_products'
# 		ordering = ['-id']

    
# 	def __str__(self):
# 		return self.product_name
		
# 	def get_absolute_url(self):
# 		return reverse('shoppingcart_detail', args=(self.slug,))	

# 	def get_success_url(self):
# 	    return reverse('shoppingcart-list')

# class Categories(models.Model):
#     parent_id = models.IntegerField(blank=True, null=True)
#     lft = models.IntegerField(blank=True, null=True)
#     rgt = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         db_table = 'shoppingcart_categories'

# class Stocks(models.Model):
#     product_id = models.IntegerField(blank=True, null=True)
#     image_id = models.IntegerField(blank=True, null=True)
#     qty = models.IntegerField(blank=True, null=True)
#     price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

#     class Meta:
#         db_table = 'shoppingcart_stocks'


# class Attributes(models.Model):
#     product_id = models.IntegerField(blank=True, null=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#     order_group = models.IntegerField(blank=True, null=True)
#     order_item = models.IntegerField(blank=True, null=True)
#     hash = models.CharField(max_length=32, blank=True, null=True)

#     class Meta:
#         db_table = 'shoppingcart_attributes'

# class ProductsCategories(models.Model):
#     product_id = models.IntegerField(primary_key=True)
#     category_id = models.IntegerField()

#     class Meta:
#         db_table = 'shoppingcart_products_categories'
#         unique_together = (('product_id', 'category_id'),)




# class StocksAttributes(models.Model):
#     stock_id = models.IntegerField(blank=True, null=True)
#     product_id = models.IntegerField(blank=True, null=True)
#     attribute_id = models.IntegerField(blank=True, null=True)
#     attribute_parent_id = models.IntegerField(blank=True, null=True)

#     class Meta:
#         db_table = 'shoppingcart_stocks_attributes'




# class ProductsSimilar(models.Model):
#     product_id = models.IntegerField(blank=True, null=True)
#     similar_id = models.IntegerField(blank=True, null=True)

#     class Meta:
#         db_table = 'shopping_cart_products_similar'
#         unique_together = (('product_id', 'similar_id'),)

# class Extras(models.Model):
#     product_id = models.IntegerField(blank=True, null=True)
#     type = models.CharField(max_length=6, blank=True, null=True)
#     price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
#     is_mandatory = models.IntegerField(blank=True, null=True)

#     class Meta:
#         db_table = 'shopping_cart_extras'


# class ExtrasItems(models.Model):
#     extra_id = models.IntegerField(blank=True, null=True)
#     price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

#     class Meta:
#         db_table = 'shopping_cart_extras_items'
