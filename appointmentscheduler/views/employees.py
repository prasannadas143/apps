from django.http import HttpResponse
from django.shortcuts import render,  HttpResponseRedirect,get_object_or_404
from appointmentscheduler.models import AppschedulerServices, AppschedulerEmployees
from  appointmentscheduler.form.employeeform import EmployeeForm
import os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt,ensure_csrf_cookie

@ensure_csrf_cookie
def services_names(request):
    services = AppschedulerServices.objects.values('id','service_name')
    # DON'T USE
    serviceslist = [dict([("name",service['service_name']), ("id",service['id'])]) for service in services ]
    return HttpResponse(json.dumps(serviceslist), content_type='application/json')

@requires_csrf_token
def employee_List(request):
    """ Displays employee information of all employees """

    template_name="employeelist.html"

    return render(request, template_name)   

@requires_csrf_token
def getemployees(request):
    """  Ajax call to get list of employeees """

    employees_info=[]
    querydata = request.GET['querydata']
    if querydata == "all":
        employees = AppschedulerEmployees.objects.all().prefetch_related('appschedulerservices_set').order_by('-id')
    elif querydata == "active":
        employees = AppschedulerEmployees.objects.filter(is_active = 1 ).prefetch_related('appschedulerservices_set').order_by('-id')
    elif querydata == "inactive":
        employees = AppschedulerEmployees.objects.filter(is_active = 0 ).prefetch_related('appschedulerservices_set').order_by('-id')
    else:
        employees = AppschedulerEmployees.objects.all().prefetch_related('appschedulerservices_set').order_by('-id')

    for employee in  employees:
        data=dict()
        data['id'] = employee.pk
        if employee.avatar.name != '' :
            data['avatar'] = employee.avatar.url
        data['emp_name'] = employee.emp_name
        data['email'] = employee.email
        data['phone'] = str(employee.phone)
        data['service_count'] = employee.service_count
        data['is_active'] = int(employee.is_active)
        employees_info.append(data)
    
    return  HttpResponse(json.dumps({"data" :employees_info }), content_type='application/json')   

@ensure_csrf_cookie
def delete_employee(request,id=None):
    """ Delete employee """

    aservc=get_object_or_404(AppschedulerEmployees,  pk=int(id) )
    aservc.delete()
    return HttpResponse(status=204)


@ensure_csrf_cookie
def delete_employees(request):
    """ Delete all selected employees """

    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        aservc=get_object_or_404(AppschedulerEmployees,  pk=int(id) )
        aservc.delete()
    return HttpResponse(status=204)

@ensure_csrf_cookie
def list_phones(request):
    """ Displays phone no of each employee """

    employees = AppschedulerEmployees.objects.values('id', 'phone')
    # DON'T USE
    listphones= [dict([("phone",str(employee['phone'])), ("id",employee['id'])]) for employee in employees ]

    return HttpResponse(json.dumps(listphones), content_type='application/json')

@ensure_csrf_cookie
def list_emails(request):
    """ Displays email  of each employee """

    employees = AppschedulerEmployees.objects.values('id', 'email')
    # DON'T USE
    listemails = [dict([("email",str(employee['email'])), ("id",employee['id'])]) for employee in employees ]

    return HttpResponse(json.dumps(listemails), content_type='application/json')

@requires_csrf_token
def add_Employee(request):
    """ create a new  employee """
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
                    svcid= request.POST[fieldname]
                    svcnstance = get_object_or_404(AppschedulerServices,  pk=int(svcid) ) 
                    employee_instance.appschedulerservices_set.add(svcnstance)
            return HttpResponseRedirect('/appointmentschduler/employeelist/')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeForm()

    template_name = "addEmployee.html"
    return render(request, template_name, {'form': form})


@requires_csrf_token
def edit_Employee(request, id):
    """ Edit  the existing employee """


    template_name = "editEmployee.html"
    appscheduleobj = get_object_or_404(AppschedulerEmployees,  pk=int(id) ) 
    defaultimg=appscheduleobj.__class__._meta.get_field('avatar').default
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
                 # implement code once permission issue gets fixes
                # if appscheduleobj.service_img.name != request.FILES['photoname']:
                #     os.remove(os.path.dirname(appscheduleobj.service_img.path))
                appscheduleobj.avatar=request.FILES['avatar']
            else :
                appscheduleobj.avatar = defaultimg
            appscheduleobj.save()
            post.save()
            employee_instance = form.instance
            for key, value in request.POST.items():
                matchobj =  re.match(r'^check\d+', key)
                if matchobj:
                    fieldname = matchobj.group()
                    serviceid= request.POST[fieldname]
                    serviceinstance = get_object_or_404(AppschedulerServices,  pk=int(serviceid) )
                    employee_instance.appschedulerservices_set.add(serviceinstance)
            return HttpResponseRedirect('/appointmentschduler/employeelist/')
    else:
        form = EmployeeForm(instance=appscheduleobj)
    return render(request,template_name, {'form': form, 'appscheduleinst': appscheduleobj, "defaultimg" : defaultimg })

@csrf_exempt
def get_Employees(request):
    employee_List = AppschedulerEmployees.objects.all()
    data = {'employeelist': employee_List}
    return HttpResponseRedirect(data)

@ensure_csrf_cookie
def associated_service_names(request,id):
    """ Get the associated employee with a service"""

    services = AppschedulerServices.objects.values('id', 'service_name')   
    # DON'T USE
    servicelist = []
    appscheduleobj = get_object_or_404(AppschedulerEmployees,  pk=int(id) ).prefetch_related('appschedulerservices_set') 
    emp_service= appscheduleobj.appschedulerservices_set.values('id')
    for service in services  :
        service_info = dict([("name",service['service_name']), ("id",service['id'])]) 
        for empl_in_service in emp_service:
            if empl_in_service['id'] == service['id'] :
                service_info['checked'] = True
        servicelist.append(service_info)
    return HttpResponse(json.dumps(servicelist), content_type='application/json')

@ensure_csrf_cookie
def deleteemployeeimage(request,id):
    """Delete image of a employee"""

    appscheduleobj= get_object_or_404(AppschedulerEmployees,  pk=int(id) )
    defaultimg =  appscheduleobj.__class__._meta.get_field('avatar').default
    oldimage =appscheduleobj.avatar.name
    oldimagepath=  os.path.dirname(appscheduleobj.avatar.path)

    appscheduleobj.avatar =  defaultimg    
    employee_default_img = '/media/' + defaultimg       
    appscheduleobj.save()
    # implement code after permission issue got fixed
    # if oldimage!= defaultimg:
    #     os.remove( oldimagepath )
    return  HttpResponse(json.dumps(employee_default_img), content_type='application/json')