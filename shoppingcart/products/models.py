from django.db import models
from django.urls import reverse

# # Create your models here.

class Categories(models.Model):
#     product_id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(default = 0)
    catagorie_name = models.CharField( max_length=255, blank=False, null=False)
    child_position =  models.IntegerField(default = 0)
    class Meta:
        db_table = 'shoppingcart_products_categories'
        ordering = ['id']

class Products(models.Model):
    PRIORITY_CHOICES = ((True, 'active'),
                        (False, 'inactive'),)
    PRODUCT_STATUS = ((True, 'Available'),
                        (False, 'Hidden'),)
    product_name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    product_desc = models.TextField(blank=False, null=False)
    product_full_desc = models.TextField(blank=False, null=False)
    product_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    product_status = models.BooleanField(choices=PRODUCT_STATUS, default=True)
    is_featured = models.BooleanField(choices=PRIORITY_CHOICES, default=False)


    is_digital = models.NullBooleanField(choices=PRIORITY_CHOICES, blank=True, default=False)
    digital_file = models.ImageField(upload_to='product',  blank=True, null=True)
    digital_name = models.CharField(max_length=255, blank=True, null=True)
    digital_expire = models.CharField( max_length=255,blank=True, null=True)
    products_categories = models.ManyToManyField(Categories, related_name="products_categories" ,blank=True, null=True )

    class Meta:
        db_table = 'shoppingcart_products'
        ordering = ['-id']


    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return '/shoppingcart/products/EditProduct/' + self.id  + '/'

    def get_success_url(self):
        return '/shoppingcart/Products/ShowProducts/'






class Attributes(models.Model):

    attr_name = models.CharField(max_length=32, blank=False, null=False)
    attr_value = models.CharField(max_length=32, blank=False, null=False)
    attribute_product = models.ForeignKey(
        'Products',  blank=True, null=True,
        related_name="attribute_product" , on_delete=models.CASCADE
    )
    class Meta:
        db_table = 'shoppingcart_attributes'
        ordering = ['id']




class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='shoppingcart_products_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    photo_product = models.ForeignKey(
        'Products',  blank=True, null=True,
        related_name="photo_product", on_delete=models.CASCADE
    )
    class Meta:
        db_table = 'shoppingcart_products_photos'
        ordering = ['id']

class Stocks(models.Model):
    qty = models.IntegerField( blank=False, null=False )
    price = models.DecimalField( blank=False, null=False, decimal_places=2, max_digits=12 )
    image = models.ForeignKey( Photo, blank=True, null=True )
    stock_product = models.ForeignKey(Products, blank=True, null=True, on_delete=models.CASCADE )
    stock_attribute = models.ManyToManyField(Attributes,  blank=True, null=True)

    class Meta:
        db_table = 'shoppingcart_stocks'
        ordering = ['id']

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
