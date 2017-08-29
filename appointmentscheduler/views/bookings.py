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
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees, AppschedulerDates,AppschedulerCountries
from datetime import datetime
from pytz import country_timezones, timezone
from tzlocal import get_localzone
import re,pytz,calendar
from datetime import datetime, timedelta
import dateutil.parser as dparser


@requires_csrf_token
def show_bookings(request):
    template_name = "bookings.html"
   
    return render(request, template_name, customer_data)

@requires_csrf_token
def addbooking(request):
    template_name = "addbooking.html"
    bookingid = "BI" + str(uuid.uuid1().node)
    todaydate= datetime.now().strftime("%Y-%m-%d")
    customer_fields = {
        "c_country": "yes",
        "c_state" : "required",
        "c_city" : "required",
        "c_zip"  : "required",
        "c_name"  : "required",
        "c_email" : "required",
        "c_phone" : "required",
        "c_address1" : "required",
        "c_address2" : "required"
    }
    # pdb.set_trace() 
    Countries = AppschedulerCountries.objects.filter(status = 1 )
    country_info = []
    for Country in reversed(list(Countries)):
        data=dict()
        data['id'] = Country.id
        data['CountryName'] = Country.CountryName
        country_info.append(data)
    return render(request, template_name,{"bookingid" : bookingid,"defaultdate" : todaydate ,
        "customer_fields" : customer_fields, "countries" : country_info})

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
            return HttpResponse(json.dumps({"error_message" : "This date is off" }), content_type='application/json')
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
        # Validate  the end_time and enable  the start_time
        times = [] 
        svc_duration = 60

        for hour in employee_info["workinghours"] :
            datestr=servicedate + " " + hour["interval"]
            hour["interval_ust"] = getust(datestr,user_timezone)
        times = employee_info["workinghours"]
        times_count = len(times) 
        i = 0
        while i < times_count-1:
            svc_end_time = times[i]["interval_ust"] + timedelta(minutes=svc_duration)
            cnt1 = i + 1
            flag = 0
            for j in range(cnt1, times_count)  :
                if svc_end_time <= times[j]["interval_ust"] :
                    if times[j-1]["status"] == 'on':
                        times[i]["end_hour"] = times[j]["interval"]
                        break;
                    elif times[j]["status"] == 'off' :
                        cnt2 = i
                        for k in range(cnt2,j+1) :
                            times[k]["status"] = "off"
                        cnt3= j+1
                        for p in range(cnt3, times_count-1):
                            if times[p]['status'] ==    'on':
                                i = p
                                flag = 1
                                break 
                
                    if flag:
                        break
                elif j == times_count-1:
                    times[i]["status"] = "off"

            if not flag:
                i = i+1
        for hour in employee_info["workinghours"] :
            del hour["interval_ust"]


    return HttpResponse(json.dumps(employeelist), content_type='application/json')

def get_serviceprice(request):
    serviceids = request.GET.getlist('serviceids[]')
    pdb.set_trace() 
    (deposit, tax, total_price, total) = (0,0,0,0)
    default_status_if_paid = "confirmed"
    default_status_if_not_paid = "pending"

    for serviceid in serviceids:
        appscheduleobj = AppschedulerServices.objects.get(id=serviceid)
        price = float(appscheduleobj.price)
        total_price += price 
        tax_percentage = 10
        deposit_percentage = 30
        deposit +=  price * (deposit_percentage/100)
        tax += price * (tax_percentage/100)
        total += price + tax
    
    return HttpResponse(json.dumps({"price" : str(price) , "total_price": total_price, "tax" : tax ,
     "deposit" : deposit,"total" : total, "default_status_if_paid": default_status_if_paid,
     "default_status_if_not_paid" : default_status_if_not_paid } ), content_type='application/json')
  

def getust( date_string,user_timezone):
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    datetime_in_utc  = datetime_with_tz.astimezone(pytz.utc)
    return datetime_in_utc



