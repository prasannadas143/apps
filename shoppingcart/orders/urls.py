from django.conf.urls import url

from .views import (
        OrderListView,
        ListOrderProducts,
        ListOrderStocks,
        InsuranceShippingTaxPrice,
        ClientAddress,
        getclients
        )

urlpatterns = [
    url(r'^$', OrderListView.as_view(), name='list'),
    url(r'^ListOrderProducts/$', ListOrderProducts, name='listorderproducts'),
    url(r'^(?P<id>\d+)/ListOrderStocks/$', ListOrderStocks, name='ListOrderStocks'),
    url(r'^InsuranceShippingTaxPrice/$', InsuranceShippingTaxPrice, name='InsuranceShippingTaxPrice'),
    url(r'^clientaddress/$', ClientAddress, name='clientaddress'),
    url(r'^getclients/$', getclients, name='getclients'),

]