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
def Product(request, id):
    templatename = "Product.html"
    return render(request, templatename , { "id" : id} )

@requires_csrf_token
def SearchProduct(request):
    pdb.set_trace()
    return HttpResponse( status=204)

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
        if productsform.is_valid():
            product_obj = productsform.save()
            for key, value in request.POST.items():
                matchobj = re.match(r'^check(\d+)', key)
                if matchobj:
                    categorie_id = matchobj.group(1)
                    categorie_instance = get_object_or_404(Categories, pk=int(categorie_id))
                    product_obj.products_categories.add( categorie_instance )
                    product_obj.save()
            return HttpResponseRedirect(product_obj.get_success_url())
    listproducts = Products.objects.all()
    # use the structure to display it on dropdown in addcatagorie
    productsform = ProductsForm()
    catagories = _catagories_datastructure()

    templatename = "AddProduct.html"
    return render(request, templatename , { "form" : productsform, "data": catagories } )

@requires_csrf_token
def GetProductDetails( request ):
    products = Products.objects.all()
    catagories = Categories.objects.all()
    data =  list( catagories.values('id', 'catagorie_name') )
    return HttpResponse( json.dumps({"data" :data }), content_type='application/json' )
@requires_csrf_token
def ListProducts(request):
    data = list()
    defaultimagefile = "product-no-img.jpg"
    search = 0
    searchqueries = list()
    if 'search' in request.POST:
        search = request.POST['search']

    if int( search ):
        if 'product' in request.POST:
            product = request.POST['product']
            if product :
                param = {'product_name' : product }
                searchqueries.append( Q(**param) )
        if 'category' in request.POST:
            category = int( request.POST['category'] )
            catagorie_obj = get_object_or_404( Categories, id= int( category ))
            catagory_related_products = catagorie_obj.products_categories.all()

        if 'status' in request.POST:
            status = request.POST['status']

            if status != '':
                status = int(request.POST['status'])
                param = {'product_status': status }
                searchqueries.append( Q(**param) )

        if 'is_digital' in request.POST:
            is_digital = int( request.POST['is_digital'] )
            param = {'is_digital': is_digital}
            searchqueries.append( Q(**param) )

        if 'is_featured' in request.POST:
            is_featured = int( request.POST['is_featured'] )
            param = {'is_featured': is_featured}
            searchqueries.append( Q(**param) )

    if 'querydata' in request.POST:
        querydata = request.POST['querydata']
        if querydata == "available":
            param = {'product_status': True }
            searchqueries.append(Q(**param))
        elif querydata == "hidden":
            param = {'product_status': False}
            searchqueries.append(Q(**param))
    if len(searchqueries) > 0:
        q = Q()
        # AND/OR awareness
        for query in searchqueries:
            q = q & query
        if q:
            # We have a Q object, return the QuerySet
            products = Products.objects.filter(q)
    else :
        products = Products.objects.all()
    if 'category' in request.POST and  'catagory_related_products' in locals() and catagory_related_products.count():
        category_ids = [ catagory_related_product.id for catagory_related_product in catagory_related_products ]
        for product in products:
            if product.id not in  category_ids:
                products = products.exclude(id = product.id)

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
    product=get_object_or_404( Products,pk=int(id ) )
    request.POST._mutable = True
    if request.POST:
        if 'status' in request.POST:
            request.POST['product_status'] = bool(int(request.POST['status']) )
        if 'is_featured' not in request.POST:
            request.POST['is_featured'] = False
        else :
            request.POST['is_featured'] = bool( request.POST['is_featured']  )

        if  not product.stocks_set.exists():
            templatename = "AddStock.html"
            return render(request, templatename)

        productsform = ProductsForm(request.POST or None, instance=product)
        if productsform.is_valid():
            product_obj = productsform.save()
            for key, value in request.POST.items():
                matchobj = re.match(r'^check(\d+)', key)
                if matchobj:
                    categorie_id = matchobj.group(1)
                    categorie_instance = get_object_or_404(Categories, pk=int(categorie_id))
                    product_obj.products_categories.add(categorie_instance)
                    product_obj.save()

    catagories = _catagories_datastructure()
    catagorieids = []
    catagoriesobjs =  product.products_categories
    if catagoriesobjs is not None:
        related_catagories = catagoriesobjs.values('id')
        catagorieids = [catagory['id'] for catagory in related_catagories]
    catagories = _catagories_datastructure()

    return render(request, templatename, {"product": product , "data" : catagories, "catagorieids" : catagorieids })

@requires_csrf_token
def DeleteProduct(request,id):
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
