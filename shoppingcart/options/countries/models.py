from django.db import models

# Create your models here.


class Countries(models.Model):
    CountryName = models.CharField(max_length=200, blank=False, null=False,unique=True)
    Alpha2 = models.CharField(max_length=6,blank=True, null=True)
    Alpha3 = models.CharField(max_length=6, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        # managed = False
        db_table = 'shoppingcart_countries'
        ordering = ['-id']
        unique_together = (('CountryName'),)
