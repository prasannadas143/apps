from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from appointmentscheduler.models import AppschedulerServices, AppschedulerEmployees
from  appointmentscheduler.form.employeeform import EmployeeForm
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt


@csrf_exempt
def employee_List(request):
    pdb.set_trace()
    employees = AppschedulerEmployees.objects.all()
    # DON'T USE
    template_name = "employeelist.html"
    return render_to_response(template_name, {'employees': employees})


@csrf_exempt
def add_Employee(request):
    # DON'T USE
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        pdb.set_trace()
        form = EmployeeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...

            # redirect to a new URL:
            form.save()

            return HttpResponse(' ')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeForm()

    template_name = "addEmployee.html"
    return render_to_response(template_name, {'form': form})


@csrf_exempt
def edit_Employee(request, id):
    template_name = "editEmployee.html"
    appscheduleobj = AppschedulerEmployees.objects.get(id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST or None, request.FILES or None, instance=appscheduleobj)
        if form.is_valid():
            post = form.save(commit=False)
            for key in request.POST:
                if hasattr(post, key):
                    setattr(post, key, request.POST[key])
            post.save()
        return HttpResponseRedirect('/services/employeelist/')
    else:
        form = EmployeeForm(instance=appscheduleobj)
    return render_to_response(template_name, {'form': form, 'appscheduleinst': appscheduleobj})


def get_Employees(request):
    employee_List = AppschedulerEmployees.objects.all()
    data = {'employeelist': employee_List}
    return HttpResponseRedirect(data)
