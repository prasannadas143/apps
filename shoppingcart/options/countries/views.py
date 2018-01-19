from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token, \
ensure_csrf_cookie,csrf_protect
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.contrib import messages
from copy import deepcopy
import pdb,os,json
from shoppingcart.options.countries.models import Countries
from shoppingcart.options.countries.form import CountriesForm



@requires_csrf_token
def CountryTemplate(request):
        templatename="CountriesList.html"

        return render(request, templatename ) 

@ensure_csrf_cookie
def CountriesList(request):
    country_info=[]

    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "all":
            listCountry = Countries.objects.all().order_by('-id')
        elif querydata == "active":
            listCountry = Countries.objects.filter(status = 1 ).order_by('-id')
        elif querydata == "inactive":
            listCountry = Countries.objects.filter(status = 0 ).order_by('-id')
    else:
        listCountry = Countries.objects.all().order_by('-id')
    for Country in listCountry:
        data=dict()
        data['id'] = Country.id
        data['CountryName'] = Country.CountryName
        data['Alpha2'] = Country.Alpha2
        data['Alpha3'] = Country.Alpha3
        data['status'] = str(Country.status)
        country_info.append(data)
    return  HttpResponse(json.dumps({"data" :country_info }), content_type='application/json')   

@requires_csrf_token
def addCountry(request):
    templatename = "AddCountry.html"  
    if request.method == "POST":
        countryform = CountriesForm(request.POST or None, request.FILES or None)
        if countryform.is_valid():
            messages.success(request, 'Added country successfully')
            countryform.save()
    else:
        countryform = CountriesForm()
    return render(request,templatename, {'countryform': countryform } )

@requires_csrf_token
def editCountry(request,id):
    templatename="EditCountry.html"
    countryobj =    get_object_or_404( Countries,pk=id)
    contextdata = dict()
    if request.method == "POST":
        countryform = CountriesForm(request.POST or None ,instance=countryobj)
        if countryform.errors:
            contextdata['countryform'] = countryform
        if countryform.is_valid():
            post = countryform.save()
            messages.success(request, 'Edited country successfully')
            # return HttpResponseRedirect(reverse('shoppingcart:CountryTemplate'))
    countryinfo = model_to_dict(countryobj)
    countryinfo['status'] = int(countryinfo['status'])
    contextdata['Country'] = countryinfo 

    return render(request,templatename, contextdata )
@ensure_csrf_cookie
def deleteCountry(request,id=None):
    aCountry=get_object_or_404( Countries,pk=id)
    aCountry.delete()
    return HttpResponse(status=204)
