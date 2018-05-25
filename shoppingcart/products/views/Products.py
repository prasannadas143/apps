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

@requires_csrf_token
def Product(request, id):
    templatename = "Product.html"
    return render(request, templatename , { "id" : id} )

@requires_csrf_token
def AddProduct(request):
    if request.method == 'POST':
        # update the  request.POST

        # Get the node structure  and get the position of child node
        request.POST._mutable = True

        if 'is_featured' in  request.POST:
            request.POST['is_featured'] = True
        else :
            request.POST['is_featured'] = False

        productsform = ProductsForm(request.POST or None)
        pdb.set_trace()

        if productsform.is_valid():
            product_obj = productsform.save()
            for key, value in request.POST.items():
                matchobj = re.match(r'^check(\d+)', key)
                if matchobj:
                    categorie_id = matchobj.group(1)
                    categorie_instance = get_object_or_404(Categories, pk=int(categorie_id))
                    product_obj.categories =  categorie_instance
                    product_obj.save()
            return HttpResponseRedirect(product_obj.get_success_url())
    listproducts = Products.objects.all()
    # use the structure to display it on dropdown in addcatagorie
    productsform = ProductsForm()
    catagories = _catagories_datastructure()

    templatename = "AddProduct.html"
    return render(request, templatename , { "form" : productsform, "data": catagories } )

@requires_csrf_token
def ListProducts(request):
    data = list()
    defaultimagefile = "product-no-img.jpg"
    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "available":
            products = Products.objects.filter( product_status = True )
        elif querydata == "hidden":
            products = Products.objects.filter( product_status = False )
        else :
            products = Products.objects.all()
    else:
        products = Products.objects.all()


    for product in products:
        productdetail = dict()
        productdetail['product_name'] = product.product_name
        productdetail['product_id'] = product.id
        productdetail['product_status'] = product.product_status
        #Get the minimum price of the stocks related to product
        stocks = product.stocks_set.all()
        stocks_dict = dict()
        stock_min_price = 0
        stock_qty = 0
        for stock in stocks:
            stocks_dict[stock.id ] = float(stock.price)
            stock_qty += stock.qty
        if len( stocks_dict ):
            stock_id_min_price = min( stocks_dict.keys() ,  key=(lambda k: stocks_dict[k]) )
            stock_min_price = stocks_dict[stock_id_min_price]
            stock_obj_min_price = get_object_or_404(Stocks , id = int( stock_id_min_price ))
            productdetail['imagepath'] = stock_obj_min_price.image.file.url
        else :
            productdetail['imagepath'] = '/media/' + defaultimagefile


        productdetail['stock_price'] = float( stock_min_price )
        productdetail['stock_qty'] = stock_qty
        if querydata == "outofstock" :
            if stock_qty:
                data.append( productdetail )
        else :
            data.append(productdetail)
    return HttpResponse(json.dumps({"data" :data }), content_type='application/json')


@requires_csrf_token
def ProductDetail(request, id):
    templatename = "ProductDetail.html"
    product=get_object_or_404( Products,pk=id )
    catagories = _catagories_datastructure()
    catagorieids = []
    catagoriesobjs =  get_object_or_404(Products, pk=int(id)).categories
    if catagoriesobjs is not None:
        related_catagories = catagoriesobjs.categories.values('id')
        catagorieids = [catagory['id'] for catagory in related_catagories]

    return render(request, templatename, {"product": product , "data" : catagories, "catagorieids" : catagorieids })

@requires_csrf_token
def DeleteProduct(request,id):
    pdb.set_trace()
    data = []
    try:
        product = get_object_or_404(Products, pk=int(id))
        # product.delete()
    except ObjectDoesNotExist:
        print("objet does not exist")
    else:
        data.append( id )
    return HttpResponse(json.dumps({"data" :data }), content_type='application/json')

@requires_csrf_token
def DeleteProducts(request):
    rowids = request.POST['rowids']
    data = []

    for id in rowids.split(','):
        try:
            product = get_object_or_404(Products, pk=int(id))
            # product.delete()
        except ObjectDoesNotExist:
            print("objet does not exist")
        else:
            data.append(id)
    return HttpResponse(json.dumps({"data" :data }), content_type='application/json')
