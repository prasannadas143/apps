from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token, \
ensure_csrf_cookie,csrf_protect
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import timezone
from copy import deepcopy
import pdb,os,json,re,pytz
from shoppingcart.clients.models import Clients,Addresses
from shoppingcart.clients.form import ClientsForm, AddressesForm
from shoppingcart.options.countries.models import Countries

@requires_csrf_token
def addClient(request):
	listCountry = Countries.objects.values('id', 'CountryName')
	templatename="AddClient.html"
	clientsform = ClientsForm()
	addressesform = AddressesForm()
	# pdb.set_trace()
	if request.method == 'POST':
		formparams= request.POST.dict()
		formfields =  list(request.POST.keys())
		request.POST._mutable = True
		request.POST.clear()
		request.POST["email"] = formparams['email']
		request.POST["client_name"] = formparams['client_name']
		request.POST["password"] = formparams['password']
		request.POST["phone"] = formparams['phone']
		request.POST["website"] = formparams['website']
		# user_timezone = request.session['visitor_timezone'][0]
		created_time  = timezone.now()
		# format = '%Y-%m-%d %H:%M %p'
		# created_time = created_time.astimezone(pytz.timezone(user_timezone)).strftime(format)
		request.POST["created"] = created_time
		request.POST["last_login"] = created_time
		if 'status' not in formparams.keys():
			request.POST["status"] = False
		else :
			request.POST["status"] = formparams['status']

		clientsform = ClientsForm(request.POST or None )

		if clientsform.is_valid():

			clientobj = clientsform.save(commit=False)
			clientobj.save()
		else :
			return render(request,templatename, {'clientsform': clientsform, \
			'addressesform' : addressesform, "countries" : listCountry } )
		request.POST.clear()

		# Get the field data  for fields from formparams to request.POST
		# Assign it to request.POST
		pdb.set_trace()
		addressids = _getaddress_count(formfields)
		address_count = len( addressids )
		for address_no in addressids:
			state_field = "state_" + str(address_no)
			country_field = "id_country_" + str(address_no)
			city_field = "city_" +  str(address_no)
			client_zip= "client_zip_" +  str(address_no)
			address_1 = "address_1" +  str(address_no)
			address_2 = "address_2" +  str(address_no)
			is_default_shipping = "default_shipping" 
			is_default_billing = "default_billing"
			request.POST.clear()
			request.POST["state"] = formparams[state_field]
			country_value = formparams[country_field]
			request.POST["city"] = formparams[city_field]
			request.POST["client_zip"] = formparams[client_zip]
			request.POST["address_1"] = formparams[address_1]
			request.POST["address_2"] = formparams[address_2]
			billingvalue = formparams["default_billing"]
			billingno = int(re.search('(\d+)',billingvalue).group())
			if int(address_no) == billingno :
				request.POST["is_default_billing"] = True
			else :
				request.POST["is_default_billing"] = False
			
			shippingvalue = formparams["default_shipping"]
			shippingno = int(re.search('(\d+)',shippingvalue).group())

			if int(address_no) == shippingno :
				request.POST["is_default_shipping"] = True
			else :
				request.POST["is_default_shipping"] = False
			
			# Submit the form and get the object
			addressesform = AddressesForm(request.POST or None )
			if addressesform.is_valid():
				addressesobj = addressesform.save(commit=False)
				addressesobj.client  = clientobj
				Countryobj = get_object_or_404( Countries,  pk=int(country_value) ) 
				addressesobj.country  = Countryobj
				addressesobj.save()
			else :
				return render(request,templatename, {'clientsform': clientsform, \
				'addressesform' : addressesform, "countries" : listCountry } )

			# Get country object and client object 
			# Assign it to the foreign key for the model 
			# clear the request.POST and again assign from formparams to request.POST
		return HttpResponseRedirect(clientobj.get_success_url())

	return render(request,templatename, {'clientsform': clientsform, \
		'addressesform' : addressesform, "countries" : listCountry } )

def _getaddress_count(formfields):
	address_num = []
	for elm in formfields :

		searchObj = re.search( r'state_(\d+)', elm, re.M|re.I)
		if searchObj:
			address_num.append( int(searchObj.group(1)) )
	return sorted(address_num)

@requires_csrf_token
def editClient(request, id=None):
	""" Edit booking """
	templatename = "EditClient.html"
	user_timezone = request.session['visitor_timezone']
	clientsform = ClientsForm()
	addressesform = AddressesForm()
	client = get_object_or_404( Clients,  pk=int(id) ) 
	errors =""
	addresses = client.address_client.all()
	listCountry = Countries.objects.values('id', 'CountryName')
	if request.method == 'POST':
		formparams= request.POST.dict()
		formfields =  list(request.POST.keys())
		request.POST._mutable = True
		request.POST.clear()
		request.POST["email"] = formparams['email']
		request.POST["client_name"] = formparams['client_name']
		request.POST["password"] = formparams['password']
		request.POST["phone"] = formparams['phone']
		request.POST["website"] = formparams['website']
		# user_timezone = request.session['visitor_timezone'][0]
		lastlogin_time  = timezone.now()
		# format = '%Y-%m-%d %H:%M %p'
		# created_time = created_time.astimezone(pytz.timezone(user_timezone)).strftime(format)
		request.POST["created"] = client.created
		request.POST["last_login"] = lastlogin_time
		if 'status' not in formparams.keys():
			request.POST["status"] = False
		else :
			request.POST["status"] = formparams['status']

		clientsform = ClientsForm(request.POST or None,instance=client )
		if clientsform.is_valid():

			clientobj = clientsform.save(commit=False)
			clientobj.save()
		else :
			return render(request,templatename, {'clientsform': clientsform, \
			'addressesform' : addressesform, "countries" : listCountry } )
		request.POST.clear()

		# Get the field data  for fields from formparams to request.POST
		# Assign it to request.POST

		addressids = _getaddress_count(formfields)
		address_count = len( addressids )
		for address_no in addressids:
			state_field = "state_" + str(address_no)
			country_field = "id_country_" + str(address_no)
			city_field = "city_" +  str(address_no)
			client_zip= "client_zip_" +  str(address_no)
			address_1 = "address_1" +  str(address_no)
			address_2 = "address_2" +  str(address_no)
			is_default_shipping = "default_shipping" 
			is_default_billing = "default_billing"
			request.POST.clear()
			request.POST["state"] = formparams[state_field]
			country_value = formparams[country_field]
			request.POST["city"] = formparams[city_field]
			request.POST["client_zip"] = formparams[client_zip]
			request.POST["address_1"] = formparams[address_1]
			request.POST["address_2"] = formparams[address_2]
			billingvalue = formparams["default_billing"]
			billingno = int(re.search('(\d+)',billingvalue).group())
			if int(address_no) == billingno :
				request.POST["is_default_billing"] = True
			else :
				request.POST["is_default_billing"] = False
			
			shippingvalue = formparams["default_shipping"]
			shippingno = int(re.search('(\d+)',shippingvalue).group())

			if int(address_no) == shippingno :
				request.POST["is_default_shipping"] = True
			else :
				request.POST["is_default_shipping"] = False
			
			# Submit the form and get the object
			addressesform = AddressesForm(request.POST or None )
			if addressesform.is_valid():
				addressesobj = addressesform.save(commit=False)
				addressesobj.client  = clientobj
				Countryobj = get_object_or_404( Countries,  pk=int(country_value) ) 
				addressesobj.country  = Countryobj
				addressesobj.save()
			else :
				return render(request,templatename, {'clientsform': clientsform, \
				'addressesform' : addressesform, "countries" : listCountry } )

			# Get country object and client object 
			# Assign it to the foreign key for the model 
			# clear the request.POST and again assign from formparams to request.POST
		addresspks = client.address_client.values('id')
		for addresspk in addresspks:
			addressobj = get_object_or_404( Addresses,  pk=int(addresspk['id']) ) 
			addressobj.delete()
		return HttpResponseRedirect(clientobj.get_success_url())	
   
   
	# pdb.set_trace()
	data = { "clientdetail" : client, "addresses" : addresses,"countries": listCountry }
	templatename = "EditClient.html"
	return render(request, templatename, data  ) 

@ensure_csrf_cookie
def list_phones(request):
    """ Displays phone no of each employee """

    clientemails = Clients.objects.values('id', 'phone')
    # DON'T USE
    listphones= [dict([("phone",str(clientemail['phone'])), ("id",clientemail['id'])]) for clientemail in clientemails ]

    return HttpResponse(json.dumps(listphones), content_type='application/json')

@ensure_csrf_cookie
def list_emails(request):
    """ Displays email  of each employee """

    clientemails = Clients.objects.values('id', 'email')
    # DON'T USE
    listemails = [dict([("email",str(clientemail['email'])), ("id",clientemail['id'])]) for clientemail in clientemails ]

    return HttpResponse(json.dumps(listemails), content_type='application/json')

@ensure_csrf_cookie
def deleteClient(request, id=None):

    # aClient=get_object_or_404( Clients,pk=id)
    # aClient.delete()
    return HttpResponse(status=204)

@ensure_csrf_cookie
def deleteClients(request):
    """ Delete list of Clients """
    # pdb.set_trace()	
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
      # aClient=get_object_or_404( Clients,pk=id)
      # aClient.delete()
      pass

    return HttpResponse(status=204)

@requires_csrf_token
def getclients(request):
	templatename="Clients.html"
	clients = Clients.objects.values('id', 'email','client_name','status')
	clientsdetails = []   
	for client in  clients.iterator():
		clientsdetail = dict()
		clientsdetail['id'] = client['id']
		clientsdetail['email'] = client['email']
		clientsdetail['client_name'] = client['client_name']
		format = '%Y-%m-%d %H:%M %p'
		clientsdetail['last_order'] = timezone.now().strftime(format)
		clientsdetail['order'] = 1
		clientsdetail['status'] = client['status']
		clientsdetails.append( clientsdetail )
	return HttpResponse(json.dumps({"data" :clientsdetails }), content_type='application/json') 

