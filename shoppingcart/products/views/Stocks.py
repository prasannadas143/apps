from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import Http404
import pdb, json, operator, re
from ..forms.StockForm import StockForm
from ..models import Stocks,Products,Photo, Attributes
from django.http import JsonResponse

def deletestocks(request):

    pdb.set_trace()
    stockids = request.POST['deletestocks']
    for stockid in stockids.split(','):
        try:
            stockobj = get_object_or_404( Stocks, id=int( stockid ))
        except ObjectDoesNotExist:
            print("objet does not exist")
        else:
            pass
            # stockobj.delete()
    return HttpResponseRedirect('/shoppingcart/Products/Stocks/')


def listStock(request ):
    stockobjs = Stocks.objects.all()
    data = list()
    for stockobj in stockobjs:
        stockdetail = dict()
        stockdetail['id'] =stockobj.id
        stockdetail['qty'] = stockobj.qty
        stockdetail['price'] = str( stockobj.price )
        imageid = stockobj.image.id
        photoobj = get_object_or_404( Photo, id=imageid )
        stockdetail['imagepath'] = photoobj.file.url
        stockdetail['imageid'] = imageid
        stockdetail['product_name'] = stockobj.stock_product.product_name
        stockdetail['product_id'] = stockobj.stock_product.id

        stock_attributes = stockobj.stock_attribute.all()
        stock_attribute_details = list()
        for stock_attribute in stock_attributes :
            stock_attribute_detail = dict()
            stock_attribute_id = stock_attribute.id
            stock_attribute_obj = get_object_or_404( Attributes , id=stock_attribute_id )
            stock_attribute_detail['attributeid'] = stock_attribute_id
            stock_attribute_detail['stock_attr_value'] = stock_attribute_obj.attr_value
            stock_attribute_detail['stock_attr_name'] = stock_attribute_obj.attr_name
            stock_attribute_details.append( stock_attribute_detail )
        stockdetail['stock_attribute_details'] = stock_attribute_details
        data.append( stockdetail )
    return HttpResponse(json.dumps({"data" :data }), content_type='application/json')
