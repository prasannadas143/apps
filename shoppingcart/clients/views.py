from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token, \
ensure_csrf_cookie,csrf_protect
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.contrib import messages
from copy import deepcopy
import pdb,os,json
from shoppingcart.clients.models import Clients,Addresses
from shoppingcart.clients.form import ClientsForm, AddressesForm
from shoppingcart.options.countries.models import Countries

@requires_csrf_token
def addClient(request):
	pdb.set_trace()
	if request.method == 'POST':
		formparams= request.POST.dict()
		request.POST._mutable = True
		request.POST.clear()
		request.POST["email"] = formparams['email']
		request.POST["password"] = formparams['password']
		request.POST["phone"] = formparams['phone']
		request.POST["website"] = formparams['website']
		request.POST["created"] = formparams['created']
		request.POST["last_login"] = formparams['last_login']
        clientform = ClientsForm(request.POST or None )
      
        if clientform.is_valid():

            clientobj = clientform.save(commit=False)
            # clientobj.service = serviceobj
            # clientobj.employee = employeeobj
            clientobj.save()


	templatename="AddClient.html"
	clientsform = ClientsForm()
	addressesform = AddressesForm()
	listCountry = Countries.objects.values('id', 'CountryName')
	return render(request,templatename, {'clientsform': clientsform, \
		'addressesform' : addressesform, "countries" : listCountry } )


@requires_csrf_token
def editClient(request, id=None):
        templatename="EditClient.html"

        return render(request, templatename ) 

@ensure_csrf_cookie
def deleteClient(request, id=None):

    aClient=get_object_or_404( Clients,pk=id)
    aClient.delete()
    return HttpResponse(status=204)
@requires_csrf_token
def Clients(request):
        templatename="Clients.html"

        return render(request, templatename ) 

@ensure_csrf_cookie
def ClientList(request):
    country_info=[]

    # if 'querydata' in request.GET:
    #     querydata = request.GET['querydata']
    #     if querydata == "all":
    #         listCountry = Countries.objects.all().order_by('-id')
    #     elif querydata == "active":
    #         listCountry = Countries.objects.filter(status = 1 ).order_by('-id')
    #     elif querydata == "inactive":
    #         listCountry = Countries.objects.filter(status = 0 ).order_by('-id')
    # else:
    #     listCountry = Countries.objects.all().order_by('-id')
    # for Country in listCountry:
    #     data=dict()
    #     data['id'] = Country.id
    #     data['CountryName'] = Country.CountryName
    #     data['Alpha2'] = Country.Alpha2
    #     data['Alpha3'] = Country.Alpha3
    #     data['status'] = str(Country.status)
    #     country_info.append(data)
    return  HttpResponse(json.dumps({"data" :country_info }), content_type='application/json')   
