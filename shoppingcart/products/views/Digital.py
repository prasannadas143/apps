from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404 , HttpResponse
from django.http import Http404
import pdb, json, operator,re,os
from ..models import Products
from ..forms.ProductsForm import ProductsForm

@requires_csrf_token
def digital(request,id ):
    templatename = "Digital.html"
    pd = get_object_or_404(Products, id=id)
    request.POST._mutable = True
    if request.POST :
        pd = get_object_or_404(Products, id= id)
        if 'digital_file' in request.FILES:
            request.POST['digital_name'] = os.path.basename( request.FILES['digital_file'].name )
        if  pd.digital_file :
            hour  =  request.POST['hour']
            minute  =  request.POST['minute']
            request.POST['digital_expire'] = hour + ":" + minute
        request.POST['product_name'] = pd.product_name
        request.POST['product_desc'] = pd.product_desc
        request.POST['product_full_desc'] = pd.product_full_desc

        productform = ProductsForm(request.POST or None , request.FILES or None,instance=pd)
        if 'is_digital' in  request.POST and request.POST['is_digital']:
            request.POST['is_digital'] = True
        else :
            request.POST['is_digital'] = False
        if productform.is_valid():
            pd = productform.save()
    productid = pd.id
    contextdata = {"productid" : productid }
    if pd.digital_expire:
        ( hour, minute ) = pd.digital_expire.split(":")
        contextdata['hour'] = hour
        contextdata['minute'] = minute
        contextdata['digital_name'] = pd.digital_name

    return render(request, templatename, contextdata )
