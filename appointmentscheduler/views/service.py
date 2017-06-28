from django.http import HttpResponse
from django.shortcuts import  render, render_to_response,HttpResponseRedirect,HttpResponse
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees
from  appointmentscheduler.form.serviceform import ServiceForm
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.core import serializers
from PIL import Image
import io
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring



@csrf_exempt
def show_services(request):
    services = AppschedulerServices.objects.all()
    # DON'T USE
    template_name="showservices.html"
    return render_to_response(template_name, {'services': services})

@csrf_exempt
def add_service(request):
    template_name = "addservice.html"
    if request.method == "POST":
        form = ServiceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            service_instance = form.instance
            for key, value in request.POST.items():
                matchobj =  re.match(r'^check\d+', key)
                if matchobj:
                    fieldname = matchobj.group()
                    empid= request.POST[fieldname]
                    empinstance = AppschedulerEmployees.objects.get(id=int(empid))
                    service_instance.emp_service.add(empinstance)
            return HttpResponseRedirect('/services/showservices/')
    else:
        form = ServiceForm()
    return render_to_response(template_name,{'form': form} )


@csrf_exempt
def edit_service(request,id):
    template_name="editservice.html"
    appscheduleobj = AppschedulerServices.objects.get(id=id)
    defaultimg=appscheduleobj.__class__._meta.get_field('service_img').default
    if request.method == "POST":
        form = ServiceForm(request.POST or None , request.FILES or None, instance=appscheduleobj)
        if form.is_valid():
            post = form.save(commit=False)
            for key in request.POST:
                if hasattr(post, key):
                    setattr(post, key , request.POST[key])
            if ( 'photoname' in request.FILES and request.FILES['photoname'] is not None):
                # imagepath = appscheduleobj.service_img.file.name
                if appscheduleobj.service_img.name != defaultimg:
                    os.remove(os.path.dirname(appscheduleobj.service_img.path))
                appscheduleobj.service_img=request.FILES['photoname']
                appscheduleobj.save()

            post.save()
            # os.remove(imagepath)
            return HttpResponseRedirect('/services/showservices/')
    else :
        form = ServiceForm( instance=appscheduleobj )
        emp_service= appscheduleobj.emp_service.all()
        return render_to_response(template_name, {'form': form, 'appscheduleinst' : appscheduleobj,"defaultimg" : defaultimg})

def deleteimage(request,id):
    #Implemented with angula js
    appscheduleobj=AppschedulerServices.objects.get(id=id)
    defaultimg =  appscheduleobj.__class__._meta.get_field('service_img').default
    oldimage =appscheduleobj.service_img.name
    oldimagepath=  os.path.dirname(appscheduleobj.service_img.path)

    appscheduleobj.service_img = defaultimg   
    if oldimage!= defaultimg:
        os.remove( oldimagepath )
    return  HttpResponse(json.dumps(defaultimg), content_type='application/json')

def delete_service(request,id):
    aservc=AppschedulerServices.objects.get(id=id)
    aservc.delete()
    return HttpResponseRedirect('/services/showservices/')

@csrf_exempt
def employee_names(request):
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    employeelist = [dict([("name",employee.emp_name), ("id",employee.id)]) for employee in employees ]

    return HttpResponse(json.dumps(employeelist), content_type='application/json')

@csrf_exempt
def associated_employee_names(request,id):
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    employeelist = []
    appscheduleobj = AppschedulerServices.objects.get(id=id)
    emp_service= appscheduleobj.emp_service.all()
    for employee in employees  :
        employee_info = dict([("name",employee.emp_name), ("id",employee.id)]) 
        for empl_in_service in emp_service:
            if empl_in_service.id == employee.id :
                employee_info['checked'] = True
        employeelist.append(employee_info)
    return HttpResponse(json.dumps(employeelist), content_type='application/json')

def instance_to_dict(instance, fields=None, exclude=None):
    """
    Returns convert a model to a  dictionary

    """
    data = {}
    
    for field in instance._meta.fields:
        if fields and field.name not in fields:
            continue
        if exclude and field.name in exclude:
            continue
        attr = field.name
        if hasattr(instance, attr):
            value = getattr(instance, attr)
            if value is not None:
                if isinstance(field, OneToOneField):
                    # knock out duplicate inherited data.
                    # must come before Foreignkey check!
                    continue
                elif isinstance(field, ForeignKey):
                    fkey_values = instance_to_dict(value)
                    for k, v in fkey_values.items():
                        data['%s.%s' % (attr, k)] = v
                    continue
                elif isinstance(field, DateField):
                    value = value.strftime('%Y-%m-%d')
                elif isinstance(field, TimeField):
                    value = value.strftime('%H-%M-%S')
                elif isinstance(field, ImageField):
                    value = value.url
        data[field.name] = value
    if 'warning' in instance._meta.many_to_many.__dict__ :
        data[field.name] = []
    else :
        for field in instance._meta.many_to_many:
            data[field.name] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
    return data