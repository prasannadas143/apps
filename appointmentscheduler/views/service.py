from django.shortcuts import  render, HttpResponseRedirect,HttpResponse, get_object_or_404
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees
from  appointmentscheduler.form.serviceform import ServiceForm
import os,json,re
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField

@requires_csrf_token
def show_services(request):
    # DON'T USE
    # for sevice in services:
    #     service_json = instance_to_dict(services)
    #     services_json.append( service_json )
    template_name="showservices.html"
    # services = AppschedulerServices.objects.values('id', 'service_name', 'price', 'length',  'is_active')
    
    return render(request, template_name )   

@ensure_csrf_cookie
def list_services(request):
    """ Displays list of  services  """
    # DON'T USE
    # for sevice in services:
    #     service_json = instance_to_dict(services)
    #     services_json.append( service_json )
    # services = AppschedulerServices.objects.values('id', 'service_name', 'price', 'length',  'is_active')
    services_info=[]
    querydata = request.GET['querydata']
    if querydata == "all":
        services = AppschedulerServices.objects.all().prefetch_related('emp_service').order_by('-id')
    elif querydata == "active":
        services = AppschedulerServices.objects.filter(is_active = 1 ).prefetch_related('emp_service').order_by('-id')
    elif querydata == "inactive":
        services = AppschedulerServices.objects.filter(is_active = 0 ).prefetch_related('emp_service').order_by('-id')
    else:
        services = AppschedulerServices.objects.all().prefetch_related('emp_service').order_by('-id')

    for service in services:
        data=dict()
        data['id'] = service.pk
        data['service_name'] = service.service_name
        data['cnt_employees'] = service.emp_service.count()
        data['price'] = float(service.price)
        data['length'] = service.length
        data['total'] = service.total
        data['is_active'] = str(service.is_active)
        services_info.append(data)
    return  HttpResponse(json.dumps({"data" :services_info }), content_type='application/json')   



@requires_csrf_token
def add_service(request):
    """ Add a new service"""

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
                    empinstance = get_object_or_404(AppschedulerEmployees,  pk=int(empid) )
                    service_instance.emp_service.add(empinstance)

            return HttpResponseRedirect('/appointmentschduler/services/')
    else:
        form = ServiceForm()
    return render(request, template_name,{'form': form } )


@requires_csrf_token
def edit_service(request,id):
    """ Edit the service"""

    template_name="editservice.html"
    appscheduleobj =  get_object_or_404(AppschedulerServices,  pk=int(id) )
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
                    empinstance = get_object_or_404( AppschedulerEmployees,  pk=int(empid) )
                    service_instance.emp_service.add(empinstance)
            # os.remove(imagepath)
            return HttpResponseRedirect('/appointmentschduler/services/')
    else :
        form = ServiceForm( instance=appscheduleobj )
    return render(request, template_name, {'form': form, 'appscheduleinst' : appscheduleobj,"defaultimg" : defaultimg})

@requires_csrf_token
def deleteimage(request,id):
    """ Delete service image"""

    appscheduleobj= get_object_or_404(AppschedulerServices,  pk=int(id) )
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

@requires_csrf_token
def delete_service(request,id=None):
    """ Delete service """

    aservc= get_object_or_404(AppschedulerServices,  pk=int(id) )
    aservc.delete()
    return HttpResponse(status=204)

    # return HttpResponseRedirect('/services/showservices/')

@ensure_csrf_cookie
def delete_services(request):
    """ Delete  selected services """

    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        aservc= get_object_or_404(AppschedulerServices,  pk=int(id))
        aservc.delete()
    return HttpResponse(status=204)

    # return HttpResponseRedirect('/services/showservices/')

@ensure_csrf_cookie
def employee_names(request):
    employees = AppschedulerEmployees.objects.values('id', 'emp_name')
    # DON'T USE
    employeelist = [dict([("name",employee['emp_name']), ("id",employee['id'])]) for employee in employees ]

    return HttpResponse(json.dumps(employeelist), content_type='application/json')

@ensure_csrf_cookie
def associated_employee_names(request,id):
    """ Get the associated employee names for a service"""

    employees = AppschedulerEmployees.objects.values('id', 'emp_name')
    # DON'T USE
    employeelist = []
    appscheduleobj =  get_object_or_404(AppschedulerServices,  pk=int(id) ).prefetch_related('emp_service')
    emp_service= appscheduleobj.emp_service.values('id')
    for employee in employees:
        employee_info = dict([("name",employee['emp_name']), ("id",employee['id'])]) 
        for empl_in_service in emp_service:
            if empl_in_service['id'] == employee['id'] :
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