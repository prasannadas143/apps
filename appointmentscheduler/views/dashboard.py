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
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, inch, landscape
from io import BytesIO
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize

@requires_csrf_token
def dashboard(request):
	template = "dashboard.html"
	return render(request, template)

@requires_csrf_token
def getdashboarddetails(request):
	template = "dashboard.html"
	user_timezone = request.session['visitor_timezone']
	selecteddate = request.GET['selecteddate']
	bkddetails = getbookingdetails(user_timezone, selecteddate )
	bookeddetails = {"bookeddetails": bkddetails}
	return JsonResponse(bookeddetails)

@requires_csrf_token
def printdashboard(request):
	user_timezone = request.session['visitor_timezone']
	selecteddate = request.GET['selecteddate']


	boookingdetails = getbookingdetails(user_timezone, selecteddate )
	file = "dashboard.pdf"
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="{}"'.format(file)
	
	buffer = BytesIO()

	doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
	doc.pagesize = landscape(A4)

	Catalog = []
	styles = getSampleStyleSheet()

	styles.wordWrap = 'CJK'
	header = Paragraph("Product Inventory" , styles['Normal'])
	Catalog.append(header)
	style = styles['Normal']

	pdfdetails  = []
	for bkditem in boookingdetails:
		head = []
		pdfrow=[]
		pdfrow.append( bkditem['hhmm'] )
		for bkd in bkditem['bookingdetail']:
			header1 = Paragraph( bkd["employee"] , styles['Normal'])
			header2 = Paragraph( bkd["servicename"] , styles['Normal'])
			header3 = Paragraph( bkd["customername"] , styles['Normal'])
			head.extend([header1, header2, header3, Spacer(1,0.2*inch)])
		pdfrow.append( head )

		pdfdetails.append( pdfrow )
		
	headings = ('Working Time', 'Booking Details')
	t = Table([headings] + pdfdetails)
	t.setStyle(TableStyle(
	                [('GRID', (0,0), (1,-1), 2, colors.black),
	                 ('LINEBELOW', (0,0), (-1,0), 2, colors.red),
	                 ('BACKGROUND', (0, 0), (-1, 0), colors.pink)]))
	Catalog.append(t) 
	doc.build(Catalog)
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response



def getbookingdetails(user_timezone, selecteddate ):
	if selecteddate == "today":
		visitor_tz = pytz.timezone(str(user_timezone[0]))
		datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
		servicedate = visitor_tz.localize(datetime_without_tz, is_dst=None).strftime("%Y-%m-%d")
	elif selecteddate == "tomorrow":
		visitor_tz = pytz.timezone(str(user_timezone[0]))
		datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
		tomorrowdate = visitor_tz.localize(datetime_without_tz, is_dst=None) + timedelta(days=1)
		servicedate = tomorrowdate.strftime("%Y-%m-%d")
	else:
		servicedate = selecteddate
		
	# get. records for the specific date.

	svc_datetime = servicedate.split('-')
	year = int(svc_datetime[0].lstrip('0') )
	month = int(svc_datetime[1].lstrip('0') )
	day = int( svc_datetime[2].lstrip('0') )
	adates = AppschedulerBookings.objects.exclude(booking_status = "cancelled")

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
		if not len(value):
			hhmmrecord = dict()
			hhmmrecord["employee"] = "--"
			hhmmrecord["servicename"] = "--"
			hhmmrecord["customername"] = "--"
			value = [hhmmrecord]
		timerow["bookingdetail"] = value
		bkddetails.append(timerow)
	return bkddetails

