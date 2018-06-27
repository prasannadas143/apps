from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import  HttpResponse, get_object_or_404
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import   HttpResponse
import json
from ..products.models import Products, Attributes, Photo, Stocks
from ..clients.views import getclients
from ..clients.models import Clients
from .models import Orders
from ..products.views.Stock import getattributes
from ..options.models import  Options
from  ..options.ShippingAndTax.models import ShippingAndTax

class OrderListView( ListView):
    template_name = "order_list.html"

    def get_queryset(self):
        return Orders.objects.get_queryset().recent()





# class LibraryView(LoginRequiredMixin, ListView):
#     template_name = 'orders/library.html'
#
#     def get_queryset(self):
#         return ProductPurchase.objects.products_by_request(self.request)  # .by_request(self.request).digital()
#
#
# class VerifyOwnership(View):
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             data = request.GET
#             product_id = request.GET.get('product_id', None)
#             if product_id is not None:
#                 product_id = int(product_id)
#                 ownership_ids = ProductPurchase.objects.products_by_id(request)
#                 if product_id in ownership_ids:
#                     return JsonResponse({'owner': True})
#             return JsonResponse({'owner': False})
#         raise Http404


def ListOrderProducts(request):
    products = Products.objects.values('id', 'product_name')
    return HttpResponse(json.dumps( list( products  ) ), content_type='application/json')

def ListOrderStocks(request, id ):
    productobj = get_object_or_404(Products, id=id)
    addcombination = 1
    showattributes = 0
    attributes = Attributes.objects.filter(attribute_product=productobj).order_by('attr_name').values()
    listattributes = getattributes(attributes)

    if not productobj.is_digital:
        if attributes.exists():
            showattributes = 1
            columnnames = [ attribute['attr_name'] for attribute in listattributes ]
            print(columnnames)
    stockobjs = Stocks.objects.filter(stock_product=productobj)

    stockdetails = []

    for stockobj in stockobjs:
        stockdetail = dict()
        stockdetail['id'] = stockobj.id
        stockdetail['qty'] = stockobj.qty
        stockdetail['price'] = str(stockobj.price)
        imageid = stockobj.image.id
        photoobj = get_object_or_404(Photo, id=imageid)
        stockdetail['imagepath'] = photoobj.file.url
        stockdetail['imageid'] = imageid
        stock_attributes = stockobj.stock_attribute.all()
        stock_attribute_details = list()
        for stock_attribute in stock_attributes:
            stock_attribute_detail = dict()
            stock_attribute_id = stock_attribute.id
            stock_attribute_obj = get_object_or_404(Attributes, id=stock_attribute_id)
            stock_attribute_detail['attributeid'] = stock_attribute_id
            stock_attribute_detail['stock_attr_value'] = stock_attribute_obj.attr_value
            stock_attribute_detail['stock_attr_name'] = stock_attribute_obj.attr_name

            stock_attribute_details.append(stock_attribute_detail)
        stockdetail['stock_attribute_details'] = stock_attribute_details
        stockdetails.append(stockdetail)
    data  = {"id": id, "stockdetails": stockdetails, "showattributes": showattributes, "attributes": listattributes}
    return JsonResponse(  data   )

def InsuranceShippingTaxPrice( request ):
    # import pdb
    # pdb.set_trace()
    # price = request.POST['price']
    # location = request.POST['location']
    price = 200
    TaxAndShippingPrice = {}
    location = "calcutta"
    options = Options.objects.filter( key="sc_insurance_fee_type").values()

    if options.exists() :
        option = options[0]
        insurancetype = option['value'].split('::')[1]
        insurance_obj = get_object_or_404( Options , key= "sc_insurance_fee" )
        insurance = insurance_obj.value
        if insurancetype == 'percent':
            insuranceprice = price * ( int( insurance )/100 )
        else :
            insuranceprice = insurance
    else :
        raise Http404
    shippingandtax = get_object_or_404(ShippingAndTax, location=location)
    tax_percentage = shippingandtax.tax
    shipping = shippingandtax.shipping
    tax = price * (tax_percentage / 100)
    extra_price = {"tax": tax, "price": float( price ), "shipping" : shipping, "insurancetype" : insurancetype, "insurance": insuranceprice }
    return JsonResponse(  extra_price  )

@requires_csrf_token
def getclients(request):
    templatename="Clients.html"
    clients = Clients.objects.values('id', 'email','client_name','phone', 'website')
    clientsdetails = []
    for client in  clients.iterator():
        clientsdetail = dict()
        clientsdetail['id'] = client['id']
        clientsdetail['email'] = client['email']
        clientsdetail['client_name'] = client['client_name']
        clientsdetail['phone'] = client['phone']
        clientsdetail['website'] = client['website']
        clientsdetails.append( clientsdetail )
    return JsonResponse( { "data": clientsdetails })

@requires_csrf_token
def ClientAddress( request):
    clientid = 10
    # clientid = request.POST['clientid']
    clientobj = get_object_or_404( Clients, id= int(clientid) )
    #Get the address details of client and return
    if clientobj.address_client.exists():
        clientaddresses = list( clientobj.address_client.values() )
    return JsonResponse({"data": clientaddresses})
