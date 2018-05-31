from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404 , HttpResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import Http404
import pdb, json, operator,re
from ..forms.ProductsForm import ProductsForm
from ..models import Products, Categories, Stocks
from .Catagories import _catagories_datastructure
from django.db.models import Q

@requires_csrf_token
def ListSimilarProducts(request):
    productid = request.POST['productid']
    productobj  = get_object_or_404( Products, id=int( productid ))
    productname = productobj.product_name
    start_product_name = productname.split()[0][:3]

    data = list()
    products = Products.objects.filter( product_name__icontains=start_product_name )
    productdetails = list()
    for product in products:
        productdetail = dict()
        productdetail['product_name'] = product.product_name
        productdetail['product_status'] = product.product_status
        productdetail['product_id'] = product.id
        productdetails.append( productdetail )
    return HttpResponse(json.dumps({"data" :productdetails }), content_type='application/json')

