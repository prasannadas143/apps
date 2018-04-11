from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404 , HttpResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import Http404
import pdb, json, operator,re
from ..forms.ProductsForm import ProductsForm
from ..models import Products, Categories
from .Catagories import _catagories_datastructure


@requires_csrf_token
def AddProduct(request):
    if request.method == 'POST':
        # update the  request.POST

        # Get the node structure  and get the position of child node
        pdb.set_trace()
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
                    product_obj.product.add( categorie_instance )

            return HttpResponseRedirect(product_obj.get_success_url())
    listproducts = Products.objects.all()
    # use the structure to display it on dropdown in addcatagorie
    productsform = ProductsForm()
    catagories = _catagories_datastructure()

    templatename = "AddProduct.html"
    return render(request, templatename , { "form" : productsform, "data": catagories } )

@requires_csrf_token
def ListProducts(request):
    data = {"data": "products"}
    templatename = "Products.html"
    return render(request, templatename, data)