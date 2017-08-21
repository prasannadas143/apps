from django.shortcuts import  render, render_to_response,HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
import datetime,pdb,os,json,re,uuid
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt,ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.core import serializers
from django.core.files import File
from django.utils.safestring import mark_safe
from django.db.models import Count
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees, AppschedulerDates
from datetime import datetime
from pytz import country_timezones, timezone
from tzlocal import get_localzone
import re,pytz,calendar
from datetime import datetime, timedelta
import dateutil.parser as dparser

@requires_csrf_token
def show_bookings(request):
    template_name = "bookings.html"

    return render(request, template_name)

@requires_csrf_token
def addbooking(request):
    template_name = "addbooking.html"
    bookingid = "BI" + str(uuid.uuid1().node)
    todaydate= datetime.now().strftime("%Y-%m-%d")
    return render(request, template_name,{"bookingid" : bookingid,"defaultdate" : todaydate })

@ensure_csrf_cookie
def employee_in_booking(request):
    serviceid = request.GET['serviceid']
    servicedate = request.GET['servicedate']
    user_timezone = request.session['visitor_timezone']

    # convert the book date to ust time
    usttime = getust(servicedate, user_timezone)
    year = usttime.year
    month = usttime.month
    day = usttime.day

    # Prepare  timestamps from start_time to end_time with 30 min gap
    #Get the working hours for the given date
    adates = AppschedulerDates.objects.filter(date__year=year)
    booktime=None
    for dt in adates:
        getvisitortime = dt.date.astimezone(pytz.timezone(user_timezone[0]))
        if getvisitortime.date().day == day and getvisitortime.date().month == month:
            booktime = dt
            break

    #Create dateobj  if the date is not available in DB
    if not booktime :
        usttime = getust(servicedate,user_timezone)
        start_time_p = "9:30 AM"
        end_time_p = "5:30 PM"
        start_launch_p = "10:30 AM"
        end_launch_p = "11:30 AM"
        # prepare default string  with default value
        start_time_string = servicedate + " " + start_time_p
        start_time = getust(start_time_string,user_timezone)
        end_time_string = servicedate + " " + end_time_p
        end_time = getust(end_time_string,user_timezone)
        start_launch_string = servicedate + " " + start_launch_p
        start_launch = getust(start_launch_string,user_timezone)
        end_launch_string = servicedate + " " + end_launch_p
        end_launch = getust(end_launch_string,user_timezone)
        adt =AppschedulerDates(date=usttime, start_time=start_time, end_time=end_time,
              start_launch=start_launch, end_launch=end_launch, is_dayoff=0, visitor_timezone=user_timezone[0]  )
        adt.save()
    else :
        if booktime.is_dayoff:
            return HttpResponse({"error_message" : "Today is off" })
        else :
            start_time = booktime.start_time
            end_time = booktime.end_time
            start_launch = booktime.start_launch
            end_launch = booktime.end_launch

    # prepare the timstamps with 30 min gap
    workinghours = []
    next_time = start_time
    while next_time <= end_time :
        # add times to working hours list
        intervaltime = dict()
        intervaltime['interval'] = next_time
        intervaltime.setdefault('status', "unknown")
        if next_time >= start_launch and next_time <= end_launch:
            intervaltime['status'] = "off"
        next_time = next_time + timedelta(minutes=30)
        workinghours.append(intervaltime)

    #Get the service duration
    serviceobj = AppschedulerServices.objects.filter(id=serviceid)[0]
    svc_duration = serviceobj.total
    for workinghour in workinghours:
        svc_start_time = workinghour['interval']
        svc_end_time = svc_start_time + timedelta(minutes=svc_duration)
        # filter the off time also "launch time " and "end time"  ( all employee )
        if svc_end_time <= end_time  and not ((svc_end_time > start_launch) and (svc_end_time < end_launch)):
            workinghour['status'] = "on"
        workinghour['interval'] = workinghour['interval'].astimezone(pytz.timezone(user_timezone[0])).strftime("%I:%M %p")
        # for interval_count in range(len(workinghours)):
        # svc_start_time = workinghours[interval_count]


    #Get all employee related to service
    employees = AppschedulerEmployees.objects.all()
    employeelist = []
    appscheduleobj = AppschedulerServices.objects.get(id=serviceid)
    emp_service = appscheduleobj.emp_service.all()
    for employee in emp_service:    
        # Mark it as off times also if  there is existing booking for the employee on the given time.

        # for empl_in_service in emp_service:
        #     if empl_in_service.id == employee.id:
        #         employee_info['checked'] = True
        # Get the working hours for the mentioned employee for the given date

        employee_info = dict([("name", employee.emp_name), ("id", employee.id),("image", employee.avatar.url),("workinghours" , workinghours)])
        employeelist.append(employee_info)

    return HttpResponse(json.dumps(employeelist), content_type='application/json')


def getust( date_string,user_timezone):
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    datetime_in_utc  = datetime_with_tz.astimezone(pytz.utc)
    return datetime_in_utc
