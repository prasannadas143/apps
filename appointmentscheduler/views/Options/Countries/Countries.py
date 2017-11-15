from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from appointmentscheduler.models import AppschedulerCountries
import pdb,os,json
from django.views.decorators.csrf import csrf_exempt
from  appointmentscheduler.form.Options.Countries.Countries import Countries
from django.forms.models import model_to_dict



@csrf_exempt
def CountryTemplate(request):
        template_name="CountriesList.html"
        templatename=  os.path.join('Options','Countries',template_name)
        return render(request, templatename ) 

@csrf_exempt
def CountriesList(request):
    country_info=[]
    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "all":
            Countries = AppschedulerCountries.objects.all().order_by('-id')
        elif querydata == "active":
            Countries = AppschedulerCountries.objects.filter(status = 1 ).order_by('-id')
        elif querydata == "inactive":
            Countries = AppschedulerCountries.objects.filter(status = 0 ).order_by('-id')
    else:
        Countries = AppschedulerCountries.objects.all().order_by('-id')

    for Country in Countries:
        data=dict()
        data['id'] = Country.id
        data['CountryName'] = Country.CountryName
        data['Alpha2'] = Country.Alpha2
        data['Alpha3'] = Country.Alpha3
        data['status'] = str(Country.status)
        country_info.append(data)
    return  HttpResponse(json.dumps({"data" :country_info }), content_type='application/json')   

@csrf_exempt
def addCountry(request):
    template_name = "AddCountry.html"  
    if request.method == "POST":
        appscheduleCountry = Countries(request.POST or None, request.FILES or None)
        if appscheduleCountry.is_valid():
            appscheduleCountry.save()
    else:
        appscheduleCountry = Countries()
    templatename=  os.path.join('Options','Countries',template_name)
    return render(request,templatename, {'appscheduleCountry': appscheduleCountry } )

@csrf_exempt
def editCountry(request,id):
    template_name="EditCountry.html"
    appscheduleobj =     AppschedulerCountries.objects.get(id=id)
    if request.method == "POST":
        appscheduleCountry = Countries(request.POST or None ,instance=appscheduleobj)
        if appscheduleCountry.is_valid():
            post = appscheduleCountry.save()
            return HttpResponseRedirect('/appointmentschduler/CountryTemplate/')
    templatename=  os.path.join('Options','Countries',template_name)
    countryinfo = model_to_dict(appscheduleobj)
    countryinfo['status'] = int(countryinfo['status'])
    return render(request,templatename, {'appscheduleCountry': countryinfo } )


@csrf_exempt
def deleteCountry(request,id=None):
    aCountry=AppschedulerCountries.objects.get(id=id)
    aCountry.delete()
    return HttpResponse(status=204)
