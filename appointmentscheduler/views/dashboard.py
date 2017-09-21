from django.shortcuts import  render, render_to_response,HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
import pdb,os,json,re,uuid
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt,ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.core import serializers
from django.core.files import File
from django.utils.safestring import mark_safe
from django.db.models import Count
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees, \
AppschedulerDates,AppschedulerCountries,AppschedulerBookings,AppschedulerInvoice
from pytz import country_timezones, timezone
from tzlocal import get_localzone
import re,pytz,calendar
from datetime import datetime, timedelta
import datetime as dtm
import dateutil.parser as dparser
from copy import deepcopy
from collections import OrderedDict

@requires_csrf_token
def dashboard(request):
	template = "dashboard.html"
	return render(request, template)

@requires_csrf_token
def getdashboarddetails(request):
	template = "dashboard.html"
	user_timezone = request.session['visitor_timezone']
	selecteddate = request.GET['selecteddate']
	if selecteddate == "today":
		visitor_tz = pytz.timezone(str(user_timezone[0]))
		datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
		servicedate = visitor_tz.localize(datetime_without_tz, is_dst=None).strftime("%Y-%m-%d")
	elif selecteddate == "tomorrow":
		visitor_tz = pytz.timezone(str(user_timezone[0]))
		datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
		tomorrowdate = visitor_tz.localize(datetime_without_tz, is_dst=None) + + dtm.timedelta(days=1)
		servicedate = tomorrowdate.strftime("%Y-%m-%d")
	else:
		servicedate = request.GET['selecteddate']
		
	# get. records for the specific date.

	svc_datetime = servicedate.split('-')
	year = int(svc_datetime[0].lstrip('0') )
	month = int(svc_datetime[1].lstrip('0') )
	day = int( svc_datetime[2].lstrip('0') )
	adates = AppschedulerBookings.objects.all()

	# Get all bookings info from the date/time/year of booking. 
	bookedtimes = []
	for dt in adates:
		getvisitortime = dt.date.astimezone(pytz.timezone(user_timezone[0])).date()
		if getvisitortime.day == day and getvisitortime.month == month and getvisitortime.year == year:
			bookedtimes.append( dt )

 
	# get the currentdates start time and end time.

	cdates = AppschedulerDates.objects.filter(date__year=year,  visitor_timezone = user_timezone[0]  )
	(cdt_obj, ctc_time, end_time) = (None, None, None)
	for cdt in cdates:
		ctime = cdt.date.astimezone(pytz.timezone(user_timezone[0]))
		if ctime.date().day == day and ctime.date().month == month:
			cdt_obj = cdt
			ctc_time = cdt_obj.start_time
			end_time = cdt_obj.end_time
			break
	bookeddetails = OrderedDict()
	if cdt_obj is not None and ctc_time is not  None and end_time is not  None:
		while(ctc_time <= end_time) :
		# search for records in current hour and minute.
			bookedhhmm = ctc_time.astimezone(pytz.timezone(user_timezone[0])).strftime( "%I:%M %p" )
			bookeddetails.setdefault(bookedhhmm, [])
			for booktime in bookedtimes:
			# check current time is sanme as booked time 
				if booktime.service_start_time.hour == ctc_time.hour and booktime.service_start_time.minute == ctc_time.minute:
					hhmmrecord = dict()
					hhmmrecord["employee"] = booktime.employee.emp_name
					hhmmrecord["servicename"] = booktime.service.service_name
					hhmmrecord["customername"] = booktime.c_name
					hhmmrecord["id"] = booktime.id

					bookeddetails.setdefault(bookedhhmm, []).append(hhmmrecord)

			ctc_time =  ctc_time + timedelta(minutes=30)
	else :

		default_day_start_str =  servicedate + " " +  "9:30 AM" 
		default_day_start_without_tz  =dparser.parse(default_day_start_str)
		default_time_with_tz = visitor_tz.localize(default_day_start_without_tz, is_dst=None)
		default_day_end_str =  servicedate + " " +  "5:30 PM" 
		default_day_end_without_tz  =dparser.parse(default_day_end_str)
		default_day_end_with_tz = visitor_tz.localize(default_day_end_without_tz, is_dst=None)
		while(default_time_with_tz <= default_day_end_with_tz) :
			bookedhhmm = default_time_with_tz.astimezone(pytz.timezone(user_timezone[0])).strftime( "%I:%M %p" )
			bookeddetails.setdefault(bookedhhmm, [])
			default_time_with_tz =  default_time_with_tz + timedelta(minutes=30)
	bkddetails = list()
	for key,value in bookeddetails.items():
		timerow = dict()
		timerow["hhmm"] = key
		timerow["bookingdetail"] = value

		bkddetails.append(timerow)
	bookeddetails = {"bookeddetails": bkddetails}
	return JsonResponse(bookeddetails)
