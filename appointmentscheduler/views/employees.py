from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from appointmentscheduler.models import AppschedulerServices, AppschedulerEmployees
from  appointmentscheduler.form.employeeform import EmployeeForm
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.core import serializers
from PIL import Image
import io
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt,ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField



@csrf_exempt
def services_names(request):
    services = AppschedulerServices.objects.all()
    # DON'T USE
    serviceslist = [dict([("name",service.service_name), ("id",service.id)]) for service in services ]
    return HttpResponse(json.dumps(serviceslist), content_type='application/json')

@csrf_exempt
def employee_List(request):
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    template_name = "employeelist.html"
    return render_to_response(template_name, {'employees': employees})


@ensure_csrf_cookie
def list_phones(request):
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    listphones= [dict([("phone",str(employee.phone)), ("id",employee.id)]) for employee in employees ]

    return HttpResponse(json.dumps(listphones), content_type='application/json')

@ensure_csrf_cookie
def list_emails(request):
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    listemails = [dict([("email",str(employee.email)), ("id",employee.id)]) for employee in employees ]

    return HttpResponse(json.dumps(listemails), content_type='application/json')

@csrf_exempt
def delete_employee(request,id=None):
    aservc=AppschedulerEmployees.objects.get(id=id)
    aservc.delete()
    return HttpResponseRedirect('/services/employeelist/')

@csrf_exempt
def add_Employee(request):
    # DON'T USE
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        form = EmployeeForm(request.POST or None, request.FILES or None)

 
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            employee_instance = form.instance
                
            for key, value in request.POST.items():
                matchobj =  re.match(r'^check\d+', key)     
                if matchobj:
                    fieldname = matchobj.group()
                    empid= request.POST[fieldname]
                    empinstance = AppschedulerServices.objects.get(id=int(empid))
                    employee_instance.appschedulerservices_set.add(empinstance)
            return HttpResponseRedirect('/appointmentschduler/employeelist/')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeForm()

    template_name = "addEmployee.html"
    return render_to_response(template_name, {'form': form})


@csrf_exempt
def edit_Employee(request, id):
    template_name = "editEmployee.html"
    appscheduleobj = AppschedulerEmployees.objects.get(id=id)
    defaultimg=appscheduleobj.__class__._meta.get_field('avatar').default
    pdb.set_trace()
    if request.method == "POST":
        form = EmployeeForm(request.POST or None, request.FILES or None, instance=appscheduleobj)
        if form.is_valid():
            post = form.save(commit=False)
            for key in request.POST:
                if hasattr(post, key):
                   
                   if key=='is_subscribed' and request.POST.get('is_subscribed') == 'true':
                      form.instance.is_subscribed = True
                      request.POST['is_subscribed']  = True
                setattr(post, key, request.POST[key])
            if 'avatar' in request.FILES and request.FILES['avatar'] is not None:
                if appscheduleobj.avatar.name != defaultimg:
                    appscheduleobj.avatar=defaultimg
                appscheduleobj.avatar=request.FILES['avatar']
                appscheduleobj.save()
            post.save()
            return HttpResponseRedirect('/services/employeelist/')
    else:
        form = EmployeeForm(instance=appscheduleobj)
    return render_to_response(template_name, {'form': form, 'appscheduleinst': appscheduleobj, "defaultimg" : defaultimg })


def get_Employees(request):
    employee_List = AppschedulerEmployees.objects.all()
    data = {'employeelist': employee_List}
    return HttpResponseRedirect(data)
