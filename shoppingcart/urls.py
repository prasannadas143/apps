from django.conf.urls import url,include
from shoppingcart.products import urls as products
from shoppingcart.clients import urls as clients

urlpatterns = [

    url(r'^Products/', include('shoppingcart.products.urls')),
    url(r'^clients/', include('shoppingcart.clients.urls')),
    url(r'^orders/', include('shoppingcart.orders.urls')),
    url(r'^dashboard/', include('shoppingcart.dashboard.urls')),
    url(r'^vouchers/', include('shoppingcart.vouchers.urls')),
    url(r'^report/', include('shoppingcart.report.urls')),
    url(r'^options/', include('shoppingcart.options.urls')),

   ]