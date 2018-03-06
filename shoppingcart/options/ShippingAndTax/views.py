from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from django.contrib import messages
from .models import ShippingAndTax
from .forms import ShippingAndTaxForm
import pdb,re
# Create your views here.

@requires_csrf_token
def addshipping(request):
	data = dict()
	if request.POST:
		fields = request.POST.keys()
		fieldscount = []
		for field in fields :
			searchObj = re.search( r'\d+', field)
			if searchObj:
			   fieldscount.append( int(searchObj.group()))
		
		   
		print( fieldscount ) 
		# shipping_info = {'location_1': ['Bangalore'], 'shipping_1': ['11'], 'free_shipping_1': ['11'], 'tax_1': ['11'], 'location_2': ['bbsr'], 'shipping_2': ['11'], 'free_shipping_2': ['11'], 'tax_2': ['11']}  
		formparams= request.POST.dict()
		request.POST._mutable = True
		request.POST.clear()
		for fieldno in  set(fieldscount):
			print(fieldno)
		# Get name of the fields 
			location = "location_" + str(fieldno)
			shipping = "shipping_" + str(fieldno)
			free_shipping = "free_shipping_" + str(fieldno)
			tax = "tax_" + str(fieldno)
			shippingid = "shippingid_" +  str(fieldno)
			print(location, shipping, free_shipping, tax)
			request.POST["location"] = formparams[location]
			request.POST["shipping"] = formparams[shipping]
			request.POST["free_shipping"] = formparams[free_shipping]
			request.POST["tax"] = formparams[tax]
			# Edit the shipping info if shipping id exist  else add shopping info
			if shippingid in formparams:
				shippingpk = formparams[shippingid]
				shipping_obj = get_object_or_404(ShippingAndTax, pk= shippingpk )
				shippingandtax_form = ShippingAndTaxForm(request.POST or None , instance = shipping_obj)
				if shippingandtax_form.is_valid():
					messages.success(request, "Updated " + request.POST["location"] + " in Shoppingcart successfully")
					shippingandtax_form.save()
			else :
				shippingandtax_form = ShippingAndTaxForm(request.POST or None )
				if shippingandtax_form.is_valid():
					messages.success(request, "Added " + request.POST["location"] + " in Shoppingcart successfully")
					shippingandtax_form.save()

			data['form'] = shippingandtax_form 
	data['shippings'] = ShippingAndTax.objects.all()

	templatename="Shipping.html"
	return render(request, templatename ,data)

@ensure_csrf_cookie
def deleteshipping(request):
	shippingandtax=get_object_or_404( ShippingAndTax,pk=int(request.POST['id']))
	shippingandtax.delete()
	return HttpResponse(status=204)
