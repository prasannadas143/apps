from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from appointmentscheduler.models import  AppschedulerWorkingTimes
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.http import JsonResponse
import pdb,os,json,re
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from pytz import country_timezones, timezone
from tzlocal import get_localzone
import re,pytz,calendar
from datetime import datetime, timedelta
import dateutil.parser as dparser
from appointmentscheduler.views.Options.WorkingTime.DefaultTime import *

global user_timezone 
def getust( date_string):
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    datetime_in_utc  = datetime_with_tz.astimezone(pytz.utc)

    return datetime_in_utc

def getdateobj( date_string):
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)

    return datetime_with_tz



def convert_to_local(dateandtime,local_timezone):
    datetime_in_pacific = dateandtime.astimezone(pytz.timezone(local_timezone[0]))
    return datetime_in_pacific.strftime("%I:%M %p")

@csrf_exempt    
def WorkingTimeOptions(request):
    global user_timezone
    ip = get_ip_address_from_request(request)   
    user_timezone = getusertimezone(ip)
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    # get time now for the specific timezone 
    visitor_time = datetime.datetime.now(visitor_tz)
   
  
    # create the objects for monday to sunday 
    # get  the object of start  of week  "monday" and end of week "sunday"
    start = visitor_time - timedelta(days=visitor_time.weekday())
    weeksrecords_visitor = []
    weeksrecords_ust = []
    #Create the objects of each day of the week 
    for i in range(7):
        weekrecord_visitor = dict()
        weekrecord_ust = dict()
        nextday =  start + timedelta(days=i)

        #prepare the defaut string for 9:30 and convert it to ust
        # start_time_ust =  getust(date_string)
        year = nextday.year
        month = nextday.month
        day = nextday.day
        # check ust datenextdaytime is available in "customtime " DB
        adate = None
        adates = AppschedulerDates.objects.filter(date__year = year  )

        for dt in adates:
            getvisitortime = dt.date.astimezone(pytz.timezone(user_timezone[0]))
            if getvisitortime.date().day == day and getvisitortime.date().month == month :
                adate = dt 
                break
        if not bool(adate):
            start_time = "9:30 AM"
            end_time = "5:30 PM"
            start_launch = "10:30 AM"
            end_launch = "11:30 AM"
        # prepare default string  with default value 
            start_time_string = nextday.strftime('%Y-%m-%d') +" " + start_time
            end_time_string = nextday.strftime('%Y-%m-%d') +" " + end_time
            start_launch_string = nextday.strftime('%Y-%m-%d') +" " + start_launch
            end_launch_string = nextday.strftime('%Y-%m-%d') +" " + end_launch
            start_date = nextday.strftime('%Y-%m-%d') 
            #Prepare the record to be filled in DB "customtime"
            ust_start_time = getust(start_time_string)
            ust_end_time = getust(end_time_string)
            ust_start_launch = getust(start_launch_string)
            ust_end_launch = getust(end_launch_string)
            ust_start_date =  getdateobj(start_date)


            #prepare the records to be displayed in webpage which is on visitor timezone
            weekrecord_visitor["start_time"] = start_time
            weekrecord_visitor["end_time"] = end_time
            weekrecord_visitor["start_launch"] = start_launch
            weekrecord_visitor["end_launch"] = end_launch
            weekrecord_visitor["week_day"] = nextday.strftime('%A')
            weekrecord_visitor["start_date"] = start_date
            weekrecord_visitor["is_dayoff"] = 0


            #prepare the data to be inserted into DB
            weekrecord_ust["start_time"] = ust_start_time
            weekrecord_ust["end_time"] = ust_end_time
            weekrecord_ust["start_launch"] = ust_start_launch
            weekrecord_ust["end_launch"] = ust_end_launch   
            weekrecord_ust["start_date"] = ust_start_date
            weekrecord_ust["is_dayoff"] = 0
            adt =AppschedulerDates(date=ust_start_date, start_time=ust_start_time, end_time=ust_end_time,
              start_launch=ust_start_launch, end_launch=ust_end_launch, is_dayoff=0  )
            adt.save()
            weeksrecords_ust.append(weekrecord_ust)
        else :
            # data['id'] = adate.pk 

            datetime_local = adate.date.astimezone(pytz.timezone(user_timezone[0]))
            weekrecord_visitor['start_date'] = datetime_local.strftime('%Y-%m-%d')
            weekrecord_visitor['start_time'] = convert_to_local(adate.start_time,user_timezone)
            weekrecord_visitor['end_time'] =  convert_to_local(adate.end_time,user_timezone)
            weekrecord_visitor['start_launch'] = convert_to_local(adate.start_launch,user_timezone)
            weekrecord_visitor['end_launch'] = convert_to_local(adate.end_launch,user_timezone)
            weekrecord_visitor["week_day"] = datetime_local.strftime('%A')
            weekrecord_visitor['is_dayoff'] = adate.is_dayoff
        weeksrecords_visitor.append(weekrecord_visitor)
    templatename=  os.path.join('Options','WorkingTime','Default.html')
    return render(request,templatename, {"weeksrecord" : weeksrecords_visitor })
  
@csrf_exempt    
def WorkingTimeOptionsEdit(request):
    global user_timezone
    ip = get_ip_address_from_request(request)   
    user_timezone = getusertimezone(ip)
    request.POST._mutable= True
    formparams= request.POST.dict()
    weeksrecords_visitor = list()
    errdict = dict()
    if request.method == "POST":
        weeksday = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday" ]
        for day in weeksday :
            errors=""
            request.POST.clear()
            start_time_key = day + "_from"
            end_time_key = day + "_to"
            launch_from_key = day + "_launch_from"
            launch_to_key = day + "_launch_to"
            is_dayoff_key= day + "_isday_off"
            date_key = day + "_date"

            custom_date = formparams[date_key]
            if not custom_date :
                pass
            else :
                custom_date_instace = datetime.datetime.strptime(custom_date, '%Y-%m-%d')

                if is_dayoff_key in formparams  and formparams[is_dayoff_key] :
                    is_dayoff = formparams[is_dayoff_key]
                    time = "00:00 AM"
                    request.POST['date'] = getust(custom_date)
                    request.POST['start_time'] = convert_to_ust(custom_date,time,ip)
                    request.POST['end_time'] = convert_to_ust(custom_date,time,ip)
                    request.POST['start_launch'] = convert_to_ust(custom_date,time,ip)
                    request.POST['end_launch'] = convert_to_ust(custom_date,time,ip)
                    request.POST['is_dayoff'] = is_dayoff

                else :
                    end_time_instance = start_time_instance = end_launch_instance = start_launch_instance = None
                    request.POST['is_dayoff'] = 0
                    request.POST['date'] = getust(custom_date)
                    
                    if not formparams[start_time_key]:
                        errors += "Start time is required \n"
                    else :
                        start_time = formparams[start_time_key]
                        start_time_instance = convert_to_ust(custom_date,start_time,ip )
                        if not start_time_instance:
                            errors += "Start time is not in valid format "
                        else :
                            request.POST["start_time"] = start_time_instance


                    if not formparams[end_time_key]:
                        errors += "End time is required \n"
                    else :
                        end_time = formparams[end_time_key]
                        end_time_instance = convert_to_ust(custom_date,end_time,ip )
                        if not end_time_instance:
                            errors += "End time is not in valid format \n"
                        else :
                            request.POST["end_time"] = end_time_instance

                    if not formparams[launch_from_key]:
                        errors += "Start launch time is required\n"
                    else :
                        start_launch = formparams[launch_from_key]
                        start_launch_instance = convert_to_ust(custom_date,start_launch,ip )
                        if not start_launch_instance:
                            errors += "Start launch is not in valid format \n"
                        else :
                            request.POST["start_launch"] = start_launch_instance


                    if  not formparams[launch_to_key]:
                        errors += "End Launch time is required\n"
                    else :          
                        end_launch = formparams[launch_to_key]
                        end_launch_instance = convert_to_ust(custom_date,end_launch,ip )
                        if not end_launch_instance:
                            errors += "End launch is not in valid format \n"
                        else :
                            request.POST['end_launch'] = end_launch_instance
                    if not errors :
                        if not  (end_time_instance > start_time_instance) :
                            errors += "End time needs to be more than start time \n"
                        if  not (end_launch_instance > start_launch_instance) :
                            errors += "End launch time needs to be more than start launch time \n"
                        if  not ((start_time_instance < start_launch_instance) and  (end_launch_instance < end_time_instance)) :
                            errors += "Launch time needs to be between  start and end working hours  \n"
                dateobj = AppschedulerDates.objects.filter(date=request.POST['date'])[0] 
                form = customtimeform(request.POST or None , instance=dateobj)
                if errors :
                    form.errors["customerror"] = errors
                if form.is_valid():
                    message = "Customtime saved"
                    form.save()
                updatedobj = AppschedulerDates.objects.filter(date=request.POST['date'])[0] 
                weekrecord_visitor = dict()
                datetime_local = updatedobj.date.astimezone(pytz.timezone(user_timezone[0]))
                weekrecord_visitor['start_date'] = datetime_local.strftime('%Y-%m-%d')
                weekrecord_visitor['start_time'] = convert_to_local(updatedobj.start_time,user_timezone)
                weekrecord_visitor['end_time'] =  convert_to_local(updatedobj.end_time,user_timezone)
                weekrecord_visitor['start_launch'] = convert_to_local(updatedobj.start_launch,user_timezone)
                weekrecord_visitor['end_launch'] = convert_to_local(updatedobj.end_launch,user_timezone)
                weekrecord_visitor["week_day"] = datetime_local.strftime('%A')
                weekrecord_visitor['is_dayoff'] = updatedobj.is_dayoff
                weeksrecords_visitor.append(weekrecord_visitor)
                if errors:
                    errdict[weekrecord_visitor["week_day"]] = errors

    contents = dict()
    contents["weeksrecord"] = weeksrecords_visitor
    for element,error in errdict.items():
        form.errors[element] = error
    if form.errors:
        contents['form'] = form
    templatename=  os.path.join('Options','WorkingTime','Default.html')

    return render(request,templatename, contents)
   
    
# def working_date_default_edit(request):
#     if request.method == 'POST':
#         my_id = request.POST.get('id', '')
#         date = request.POST.get('date', '')
#         start_time = request.POST.get('start_time', '')
#         end_time = reques1t.POST.get('end_time', '')
#         start_lunch = request.POST.get('start_lunch', '')
#         end_lunch = request.POST.get('end_lunch', '')
#         is_day_off = request.POST.get('is_day_off', '')
#         scheduler_date = SchedulerDate.objects.get(id=my_id)
#         scheduler_date.date=date
#         scheduler_date.start_time=start_time
#         scheduler_date.end_time=end_time
#         scheduler_date.start_lunch=start_lunch
#         scheduler_date.end_lunch=end_lunch
#         scheduler_date.is_day_off=is_day_off
#         scheduler_date.save()
#     return HttpResponseRedirect('/')


# def working_time_default(request):
#     if request.method == 'POST':
#         form = SchedulerTimeForm(request.POST)
#         scheduler_time = form.save(commit=False)
#         scheduler_time.save()
#     return HttpResponseRedirect('/')

