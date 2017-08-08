from django.http import HttpResponse
from django.shortcuts import  render, render_to_response,HttpResponseRedirect,HttpResponse
from appointmentscheduler.models  import AppschedulerDates
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt,ensure_csrf_cookie
from django.db.models.fields import DateField, TimeField
from appointmentscheduler.form.Options.WorkingTime.DefaultTimeForm import customtimeform
from datetime import datetime
import datetime,re,pytz,calendar
from django.contrib.gis.geoip2 import GeoIP2
from easy_timezones.utils import get_ip_address_from_request, is_valid_ip, is_local_ip
from pytz import country_timezones
import dateutil.parser as dparser


timezone = 'America/Los_Angeles' 

@requires_csrf_token
def ShowCustomtimes(request):
    customtimes_info =[]
    querydata = "all"
    if 'querydata' in request.GET:
    	querydata = request.GET['querydata']
    if querydata == "all":
        customrecords = AppschedulerDates.objects.all()
    elif querydata == "yes":
        customrecords = AppschedulerDates.objects.filter(is_dayoff = 1 )
    elif querydata == "no":
        customrecords = AppschedulerDates.objects.filter(is_dayoff = 0 )
    else:
        customrecords = AppschedulerDates.objects.all()
    ip = get_ip_address_from_request(request)
    user_timezone = getusertimezone(ip)
    for customtime in reversed(list(customrecords)):
        data=dict()
        data['id'] = customtime.pk	
        datetime_in_pacific = customtime.date.astimezone(pytz.timezone(user_timezone[0]))

        data['date'] = datetime_in_pacific.strftime('%Y-%m-%d')
        data['start_time'] = convert_to_local(customtime.start_time,user_timezone)
        data['end_time'] =  convert_to_local(customtime.end_time,user_timezone)
        data['start_launch'] = convert_to_local(customtime.start_launch,user_timezone)
        data['end_launch'] = convert_to_local(customtime.end_launch,user_timezone)
        data['is_dayoff'] = str(customtime.is_dayoff)
        customtimes_info.append(data)
    return  HttpResponse(json.dumps({"data" :customtimes_info }), content_type='application/json')   


@requires_csrf_token
def CustomtimeOptions(request, id=None):
	template_name = os.path.join('Options','WorkingTime','Custom.html')
	ip = get_ip_address_from_request(request)
	request.session['visitorip'] = ip
	errors = ""
	if request.method == "POST":
		if not request.POST['date'] :
			pass
		else :
			custom_date = request.POST['date']
			custom_date_instace = datetime.datetime.strptime(custom_date, '%Y-%m-%d')
				
			if 'is_dayoff' in request.POST :
				is_dayoff = request.POST['is_dayoff']
				dayoff_string = custom_date + ' ' + "00:00 AM"
				datetime_indayoff  = dparser.parse(dayoff_string)
				request.POST['date'] = custom_date_instace
				request.POST['start_time'] = datetime_indayoff
				request.POST['end_time'] = datetime_indayoff
				request.POST['start_launch'] = datetime_indayoff
				request.POST['end_launch'] = datetime_indayoff

			else :
				end_time_instance = start_time_instance = end_launch_instance = start_launch_instance = None
				request.POST['is_dayoff'] = 0
				if not request.POST['start_time']:
					errors += "Start time is required \n"
				else :
					start_time = request.POST['start_time']
					start_time_instance = convert_to_ust(custom_date,start_time,ip )
					if not start_time_instance:
						errors += "Start time is not in valid format "
					request.POST['start_time'] = start_time_instance


				if not request.POST['end_time']:
					errors += "End time is required \n"
				else :
					end_time = request.POST['end_time']
					end_time_instance = convert_to_ust(custom_date,end_time,ip )
					if not end_time_instance:
						errors += "End time is not in valid format \n"
					else :
						request.POST['end_time'] = end_time_instance

				if not request.POST['start_launch']:
					errors += "Start launch time is required\n"
				else :
					start_launch = request.POST['start_launch']
					start_launch_instance = convert_to_ust(custom_date,start_launch,ip )
					if not start_launch_instance:
						errors += "Start launch is not in valid format \n"
					else :
						request.POST['start_launch'] = start_launch_instance


				if  not request.POST['end_launch']:
					errors += "End Launch time is required\n"
				else :			
					end_launch = request.POST['end_launch']
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

		if id is not None :
			dateobj = AppschedulerDates.objects.get(id=id)
			form = customtimeform( request.POST or None , instance=dateobj )
		else :
			form = customtimeform(request.POST or None )

		if errors :
			form.errors["customerror"] = errors
		if form.is_valid():
			message = "Customtime saved"
			form.save()
	elif id is not None :
		dateobj = AppschedulerDates.objects.get(id=id)
		user_timezone = getusertimezone(ip)
		data=dict()
		data['id'] = dateobj.pk	
		datetime_in_pacific = dateobj.date.astimezone(pytz.timezone(user_timezone[0]))

		data['date'] = datetime_in_pacific.strftime('%Y-%m-%d')
		data['start_time'] = convert_to_local(dateobj.start_time,user_timezone)
		data['end_time'] =  convert_to_local(dateobj.end_time,user_timezone)
		data['start_launch'] = convert_to_local(dateobj.start_launch,user_timezone)
		data['end_launch'] = convert_to_local(dateobj.end_launch,user_timezone)
		data['is_dayoff'] = dateobj.is_dayoff
		return render(request, template_name,{"dateobj": data , "id": id }  )


	else :
		form = customtimeform()


	return render(request, template_name,{"form": form }  )



def get_ip_address_from_request(request):
    """ Makes the best attempt to get the client's real IP or return the loopback """
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    return ip_address

def convert_to_ust(custom_date,time,ip):

	format = '%Y-%m-%d %H:%M %p'
		# try:
	#get the date input and remove space
	custom_date = custom_date.replace(" ", "")

	#Get the time input and remove space
	time = time.replace(" ", "")

	# time.strptime(time, '%H:%M%p')
	# add  periods and time
	date_string = custom_date + ' ' + time

	#Get the timezone 
	user_timezone = getusertimezone(ip)


	#Convert user timezone to utc timezone 
	try:
		user_timezone_instance = pytz.timezone(user_timezone[0])
		datetime_without_tz  = dparser.parse(date_string)
		user_time = user_timezone_instance.localize(datetime_without_tz)
		datetime_in_utc  = user_time.astimezone(pytz.utc)
	except ValueError:
	    return False
	else:
		return  datetime_in_utc 
		# 	return True
		# except ValueError:
		# 	return False


# def validate_customtime(start_time, end_time):

def convert_to_local(dateandtime,local_timezone):
	datetime_in_pacific = dateandtime.astimezone(pytz.timezone(local_timezone[0]))
	return datetime_in_pacific.strftime("%I:%M %p")

def getusertimezone(ip):
	g = GeoIP2()
	geoinfo = g.city('74.125.79.147')
	return country_timezones[geoinfo['country_code']]

def DeleteCustomtime(request, id):
	adate = AppschedulerDates.objects.filter(id = id)
	adate.delete()
	return HttpResponse(status=204)

@ensure_csrf_cookie
def DeleteCustomtimes(request):
	deleteids= request.POST['rowids']
	for id in deleteids.split(",") :
	    adate=AppschedulerDates.objects.get(id=id)
	    adate.delete()
	return HttpResponse(status=204)


