import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils import timezone

from ..clients.models import Addresses
# from billing.models import BillingProfile
# from carts.models import Cart
from ..Utils import unique_order_id_generator
from ..options.countries.models import Countries
from ..clients.models import Clients
from  ..products.models import Products, Stocks

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-created", "-timestamp")

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        # recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status='shipped')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data': recent_data,
            # 'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7  # days_ago_start = 49
        days_ago_end = days_ago_start - (number_of_weeks * 7)  # days_ago_end = 49 - 14 = 35
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(created__gte=start_date)
        return self.filter(created__gte=start_date).filter(created__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(created__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))



    def by_status(self, status="shipped"):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status='refunded')

    # def by_request(self, request):
    #     billing_profile, created = BillingProfile.objects.new_or_get(request)
    #     return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)


# Random, Unique
class Orders(models.Model):
    # billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True)  # AB31DE3
    shipping_address = models.ForeignKey(Addresses, related_name="shipping_address", null=True, blank=True)
    billing_address = models.ForeignKey(Addresses, related_name="billing_address", null=True, blank=True)
    # cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)

    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)
    insurance = models.DecimalField(max_digits=9, decimal_places=2)
    shipping = models.DecimalField(max_digits=9, decimal_places=2)
    tax = models.DecimalField(max_digits=9, decimal_places=2)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    order_country = models.ForeignKey(
        Countries, related_name="order_country", related_query_name="order_country"
    )

    order_client = models.ForeignKey(
        Clients, related_name="order_client", related_query_name="order_client"
    )
    order_stocks = models.ManyToManyField( Stocks, related_name="order_stocks", null=True, blank=True )

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-created']

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"

    # def update_total(self):
    #     cart_total = self.cart.total
    #     shipping_total = self.shipping_total
    #     new_total = math.fsum([cart_total, shipping_total])
    #     formatted_total = format(new_total, '.2f')
    #     self.total = formatted_total
    #     self.save()
    #     return new_total

    def check_done(self):
        shipping_address_required = not self.cart.is_digital
        shipping_done = False
        if shipping_address_required and self.shipping_address:
            shipping_done = True
        elif shipping_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_done and billing_address and total > 0:
            return True
        return False




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    if instance.shipping_address and not instance.shipping_address_final:
        instance.shipping_address_final = instance.shipping_address.get_address()

    if instance.billing_address and not instance.billing_address_final:
        instance.billing_address_final = instance.billing_address.get_address()


pre_save.connect(pre_save_create_order_id, sender=Orders)



class ShoppingCartOrdersStock(models.Model):
    orders_product = models.ForeignKey(
        Products, related_name="orders_product", related_query_name="orders_product"
    )

    orders_stock = models.ForeignKey(
        Stocks, related_name="orders_stock", related_query_name="orders_stock"
    )

    qty = models.IntegerField()

    order = models.ForeignKey(
        Orders, related_name="order", related_query_name="orders"
    )
