from django.http import HttpResponse
from django.shortcuts import  render, render_to_response,HttpResponseRedirect,HttpResponse
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees
from  appointmentscheduler.form.serviceform import ServiceForm
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt,ensure_csrf_cookie
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
from django.utils.safestring import mark_safe
from django.db.models import Count



@requires_csrf_token
def show_services(request):
    # DON'T USE
    # for sevice in services:
    #     service_json = instance_to_dict(services)
    #     services_json.append( service_json )
    template_name="showservices.html"
    # services = AppschedulerServices.objects.values('id', 'service_name', 'price', 'length',  'is_active')
    services = AppschedulerServices.objects.all()
    services_info=[]
    for service in reversed(list(services)):
        data=dict()
        data['id'] = service.pk
        data['service_name'] = service.service_name
        data['cnt_employees'] = service.emp_service.count()
        data['price'] = float(service.price)
        data['length'] = service.length
        data['total'] = service.total
        data['is_active'] = str(service.is_active)
        services_info.append(data)
    
    return render(request, template_name, { "services" : mark_safe(services_info) } )   



@requires_csrf_token
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

            return HttpResponseRedirect('/appointmentschduler/showservices/')
    else:
        form = ServiceForm()
    return render(request, template_name,{'form': form } )


@requires_csrf_token
def edit_service(request,id):
    template_name="editservice.html"
    appscheduleobj =     AppschedulerServices.objects.get(id=id)
    defaultimg=appscheduleobj.__class__._meta.get_field('service_img').default
    if request.method == "POST":
        form = ServiceForm(request.POST or None , request.FILES or None, instance=appscheduleobj)
        if form.is_valid():
            post = form.save()
            for key in request.POST:
                if hasattr(post, key):
                    setattr(post, key , request.POST[key])
            if ( 'photoname' in request.FILES and request.FILES['photoname'] is not None):
                # implement code once permission issue gets fixes
                # if appscheduleobj.service_img.name != request.FILES['photoname']:
                #     os.remove(os.path.dirname(appscheduleobj.service_img.path))
                appscheduleobj.service_img=request.FILES['photoname']
            else :
                appscheduleobj.avatar = defaultimg
            appscheduleobj.save()
            post.save()
            service_instance = form.instance
            for key, value in request.POST.items():
                matchobj =  re.match(r'^check\d+', key)
                if matchobj:
                    fieldname = matchobj.group()
                    empid= request.POST[fieldname]
                    empinstance = AppschedulerEmployees.objects.get(id=int(empid))
                    service_instance.emp_service.add(empinstance)
            # os.remove(imagepath)
            return HttpResponseRedirect('/appointmentschduler/showservices/')
    else :
        form = ServiceForm( instance=appscheduleobj )
    return render(request, template_name, {'form': form, 'appscheduleinst' : appscheduleobj,"defaultimg" : defaultimg})

@requires_csrf_token
def deleteimage(request,id):
    #Implemented with angula js
    appscheduleobj=AppschedulerServices.objects.get(id=id)
    defaultimg =  appscheduleobj.__class__._meta.get_field('service_img').default
    oldimage =appscheduleobj.service_img.name
    oldimagepath=  os.path.dirname(appscheduleobj.service_img.path)

    appscheduleobj.service_img = defaultimg   
    employee_default_img = '/media/' + defaultimg       

    appscheduleobj.save()
    # implement code after permission issue got fixed
    # if oldimage!= defaultimg:
    #     os.remove( oldimagepath )
    return  HttpResponse(json.dumps(employee_default_img), content_type='application/json')

@ensure_csrf_cookie
def delete_service(request,id=None):
    aservc=AppschedulerServices.objects.get(id=id)
    aservc.delete()
    return HttpResponse(status=204)

    # return HttpResponseRedirect('/services/showservices/')

@ensure_csrf_cookie
def delete_services(request):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        aservc=AppschedulerServices.objects.get(id=id)
        # aservc.delete()
    return HttpResponse(status=204)

    # return HttpResponseRedirect('/services/showservices/')

@ensure_csrf_cookie
def employee_names(request):
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    employeelist = [dict([("name",employee.emp_name), ("id",employee.id)]) for employee in employees ]

    return HttpResponse(json.dumps(employeelist), content_type='application/json')

@ensure_csrf_cookie
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