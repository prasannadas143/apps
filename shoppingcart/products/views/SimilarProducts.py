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
def SimilarProducts(request,id):
    templatename = "SimilarProducts.html"
    return render(request, templatename, {"productid" : id} )

@requires_csrf_token
def ListSimilarProducts(request):
    productid = request.POST['productid']
    productobj  = get_object_or_404( Products, id=int( productid ))
    productdetails = list()

    catagories = productobj.products_categories.all()
    list_products = dict()
    for catagorie in catagories :
        ct_products = catagorie.products_categories.all()
        for ct_product in ct_products :
            list_products[ct_product.id] = ct_product

    for productid in list_products:
        product = list_products[ productid ]
        productdetail = dict()

        productdetail['product_name'] = product.product_name
        productdetail['product_status'] = product.product_status
        productdetail['product_id'] = product.id
        productdetails.append( productdetail )

    return HttpResponse(json.dumps({ "data" :productdetails }), content_type='application/json')

