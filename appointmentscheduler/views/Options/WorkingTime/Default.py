from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from appointmentscheduler.models import  AppschedulerWorkingTimes
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.core import serializers
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField


def WorkingTimeOptions(request):
    pdb.set_trace();
    defaulttime = AppschedulerWorkingTimes.objects.all()[0]

    if request.method == 'POST':
        defaultTimeid = defaulttime.id;

        #Monday

        monday_from = request.POST['monday_from']
        defaultTimeid.monday_from=monday_from

        monday_to = request.POST['monday_to']
        defaultTimeid.monday_to=monday_to
        
        monday_launch_from = request.POST['monday_lunch_from']
        defaultTimeid.monday_launch_from=monday_launch_from

        monday_lunch_to = request.POST['monday_lunch_to']
        defaultTimeid.monday_lunch_to=monday_lunch_to
        
        monday_day_off = request.POST['monday_day_off']
        defaultTimeid.monday_day_off=monday_day_off

        #Tuesday

        tuesday_from = request.POST['tuesday_from']
        defaultTimeid.tuesday_from=tuesday_from


        tuesday_to = request.POST['tuesday_to']
        defaultTimeid.tuesday_to=tuesday_to

        tuesday_launch_from = request.POST['tuesday_lunch_from']
        defaultTimeid.tuesday_lunch_from=tuesday_lunch_from

        tuesday_lunch_to = request.POST['tuesday_lunch_to']
        defaultTimeid.tuesday_lunch_to=tuesday_lunch_to


        tuesday_day_off = request.POST['tuesday_day_off']
        defaultTimeid.tuesday_day_off=tuesday_day_off


        #wednesday
        wednesday_from = request.POST['wednesday_from']
        defaultTimeid.wednesday_from=wednesday_from

        wednesday_to = request.POST['wednesday_to']
        defaultTimeid.wednesday_to=wednesday_to

        wednesday_launch_from = request.POST['wednesday_lunch_from']
        defaultTimeid.wednesday_lunch_from=wednesday_lunch_from

        wednesday_lunch_to = request.POST['wednesday_lunch_to']
        defaultTimeid.wednesday_lunch_to=wednesday_lunch_to


        wednesday_day_off = request.is_day_off['wednesday_day_off']
        defaultTimeid.wednesday_day_off=wednesday_day_off

        #thursday

        thursday_from = request.POST['thursday_from']
        defaultTimeid.thursday_from=thursday_from

        thursday_to = request.POST['thursday_to']
        defaultTimeid.thursday_to=thursday_to

        thursday_launch_from = request.POST['thursday_lunch_from']
        defaultTimeid.thursday_lunch_from=thursday_launch_from

        thursday_lunch_to = request.POST['thursday_lunch_to']
        defaultTimeid.thursday_lunch_to=thursday_lunch_to

        thursday_day_off = request.is_day_off['thursday_day_off']
        defaultTimeid.thursday_day_off=thursday_day_off

        #friday

        friday_from = request.POST['friday_from']
        defaultTimeid.friday_from=friday_from

        friday_to = request.POST['friday_to']
        defaultTimeid.friday_to=friday_to

        friday_launch_from = request.POST['friday_lunch_from']
        defaultTimeid.friday_lunch_from=friday_launch_from

        friday_lunch_to = request.POST['friday_lunch_to']
        defaultTimeid.friday_lunch_to=friday_lunch_to

        friday_day_off = request.is_day_off['friday_day_off']
        defaultTimeid.friday_day_off=friday_day_off

        #saturday
        saturday_from = request.POST['saturday_from']
        defaultTimeid.saturday_from=saturday_from

        saturday_to = request.POST[' saturday_to']
        defaultTimeid.saturday_to=saturday_to

        saturday_lunch_from = request.POST['saturday_lunch_from']
        defaultTimeid.saturday_to=saturday_lunch_from

        saturday_lunch_to = request.POST['saturday_lunch_to']
        defaultTimeid.saturday_lunch_to=saturday_lunch_to

        saturday_day_off = request.is_day_off['saturday_day_off']
        defaultTimeid.saturday_day_off=saturday_day_off


        #sunday
        sunday_from = request.POST['sunday_from']
        defaultTimeid.sunday_from=sunday_from

        sunday_to = request.POST['sunday_to']
        defaultTimeid.sunday_to=sunday_to

        sunday_lunch_from = request.POST['sunday_lunch_from']
        defaultTimeid.sunday_lunch_from=sunday_lunch_from

        sunday_lunch_to = request.POST['sunday_lunch_to']
        defaultTimeid.sunday_lunch_to=sunday_lunch_to

        sunday_day_off = request.is_day_off['sunday_day_off']
        defaultTimeid.sunday_day_off=sunday_day_off
        
        defaultTimeid.save();

    templatename = 'Default.html'
    context = {
        'form30': AppschedulerWorkingTimes.objects.last(),
    }
    templatename=  os.path.join('Options','WorkingTime',templatename)
    return render(request,templatename, context)

def working_date_default(request):
    if request.method == 'POST':
        date = request.POST.get('date', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        start_lunch = request.POST.get('start_lunch', '')
        end_lunch = request.POST.get('end_lunch', '')
        is_day_off = request.POST.get('is_day_off', '')

        scheduler_date = AppschedulerWorkingTimes(date=date,start_time=start_time,end_time=end_time,start_lunch=start_lunch,end_lunch=end_lunch,is_day_off=is_day_off)
        scheduler_date.save()
    return HttpResponseRedirect('/')

    
def working_date_default_edit(request):
    if request.method == 'POST':
        my_id = request.POST.get('id', '')
        date = request.POST.get('date', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        start_lunch = request.POST.get('start_lunch', '')
        end_lunch = request.POST.get('end_lunch', '')
        is_day_off = request.POST.get('is_day_off', '')
        scheduler_date = SchedulerDate.objects.get(id=my_id)
        scheduler_date.date=date
        scheduler_date.start_time=start_time
        scheduler_date.end_time=end_time
        scheduler_date.start_lunch=start_lunch
        scheduler_date.end_lunch=end_lunch
        scheduler_date.is_day_off=is_day_off
        scheduler_date.save()
    return HttpResponseRedirect('/')


def working_time_default(request):
    if request.method == 'POST':
        form = SchedulerTimeForm(request.POST)
        scheduler_time = form.save(commit=False)
        scheduler_time.save()
    return HttpResponseRedirect('/')

