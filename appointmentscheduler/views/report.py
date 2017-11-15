from django.shortcuts import  render,HttpResponse,get_object_or_404
import datetime,json
from django.views.decorators.csrf import requires_csrf_token,ensure_csrf_cookie
from appointmentscheduler.models  import  AppschedulerBookings
from datetime import datetime
from appointmentscheduler.views.Options.WorkingTime.DefaultTime import convert_to_ust
from django.db.models import Count, Sum

@requires_csrf_token
def employee_report(request):
	template_name = "report_employees.html"
	return render(request, template_name )

@requires_csrf_token
def service_report(request):
	template_name = "report_services.html"
	return render(request, template_name )

@ensure_csrf_cookie
def service_report_details(request):
	error = ""
	employeeid = ""
	if "employeeid" in request.POST:
		employeeid = request.POST['employeeid'] 
		if employeeid :
			employeeid = int( request.POST['employeeid'] )
	index = request.POST['index']
	fromdate =  request.POST['fromdate'] 
	todate =  request.POST['todate'] 
	(fromdate_instance, todate_instance) =(None,None)
	time = "00:00 AM"
	user_timezone = request.session['visitor_timezone']

	if validate_date(fromdate):
		fromdate_instance = convert_to_ust(fromdate,time,user_timezone)
	if validate_date(todate):
		todate_instance = convert_to_ust(todate,time,user_timezone)
	if type(employeeid) is int :
		allbookings = AppschedulerBookings.objects.filter( employee = employeeid).select_related('employee'	,	'service')
	else :
		allbookings = AppschedulerBookings.objects.all().select_related('employee'	,	'service')

	if fromdate_instance is not None and todate_instance is not None :
		allbookings_of_dates = allbookings.filter(date__gte=fromdate_instance, date__lte=todate_instance)
	elif fromdate_instance is not None :
		allbookings_of_dates = allbookings.filter(date__gte=fromdate_instance)
	elif todate_instance is not None :
		allbookings_of_dates = allbookings.filter( date__lte=todate_instance )
	else :
		allbookings_of_dates = allbookings

	bookings_all = allbookings_of_dates.values('service__id','service__service_name')
	bookings_confirmed = allbookings_of_dates.filter( booking_status="confirmed").values('service__id'\
		,'service__service_name')
	bookings_pending = allbookings_of_dates.filter( booking_status="pending").values('service__id'\
		,'service__service_name')
	bookings_cancelled = allbookings_of_dates.filter( booking_status="cancelled").values('service__id'\
		,'service__service_name')
	
	reports = []
	reports_summary = dict()
	if index == "count" :
		bookings_all = bookings_all.annotate(booking_count=Count('service__id')).order_by('-booking_count')
		bookings_confirmed = bookings_confirmed.annotate(booking_count=Count('service__id'))
		bookings_pending = bookings_pending.annotate(booking_count=Count('service__id'))
		bookings_cancelled = bookings_cancelled.annotate(booking_count=Count('service__id'))
		for booking in bookings_all.iterator():
			report = dict()
			service_name = booking['service__service_name'] 
			report["service_name"] = service_name
			report["all"] = booking['booking_count'] 
			#get booking_count for bookings_confirmed for the employeename, if not set it to zero.
			report["confirmed"] = getbookingcount_service( bookings_confirmed, service_name )
			report["pending"] = getbookingcount_service( bookings_pending, service_name )
			report["cancelled"] = getbookingcount_service( bookings_cancelled, service_name )
			reports.append(report)
	else : 
		bookings_all = bookings_all.annotate(booking_amount=Sum('booking_total')).order_by('-booking_amount')
		bookings_confirmed = bookings_confirmed.annotate(booking_amount=Sum('booking_total'))
		bookings_pending = bookings_pending.annotate(booking_amount=Sum('booking_total'))
		bookings_cancelled = bookings_cancelled.annotate(booking_amount=Sum('booking_total'))
		for booking in bookings_all.iterator():
			report = dict()
			service_name = booking['service__service_name'] 
			report["service_name"] = service_name
			report["all"] =   round(float(booking['booking_amount']),2)
			#get booking_count for bookings_confirmed for the employeename, if not set it to zero.
			report["confirmed"] = getbookingtotal_service( bookings_confirmed, service_name )
			report["pending"] = getbookingtotal_service( bookings_pending, service_name )
			report["cancelled"] = getbookingtotal_service( bookings_cancelled, service_name )
			reports.append(report)
	reports_summary["bookings"] = reports
	reports_summary["graph"] = graph_service_data(reports)
	return  HttpResponse(json.dumps({"reports" :reports_summary }), content_type='application/json') 


@ensure_csrf_cookie
def employee_report_details(request):
	error = ""
	serviceid = ""
	if "serviceid" in request.POST:
		serviceid = request.POST['serviceid'] 
		if serviceid :
			serviceid = int( request.POST['serviceid'] )
	index = request.POST['index']
	fromdate =  request.POST['fromdate'] 
	todate =  request.POST['todate'] 
	(fromdate_instance, todate_instance) =(None,None)
	time = "00:00 AM"
	user_timezone = request.session['visitor_timezone']

	if validate_date(fromdate):
		fromdate_instance = convert_to_ust(fromdate,time,user_timezone)
	if validate_date(todate):
		todate_instance = convert_to_ust(todate,time,user_timezone)
	if type(serviceid) is int :
		allbookings = AppschedulerBookings.objects.filter( service = serviceid).select_related('employee'\
			,'service')
	else :
		allbookings = AppschedulerBookings.objects.all().select_related('employee'	,	'service')

	if fromdate_instance is not None and todate_instance is not None :
		allbookings_of_dates = allbookings.filter(date__gte=fromdate_instance, date__lte=todate_instance)
	elif fromdate_instance is not None :
		allbookings_of_dates = allbookings.filter(date__gte=fromdate_instance)
	elif todate_instance is not None :
		allbookings_of_dates = allbookings.filter( date__lte=todate_instance )
	else :
		allbookings_of_dates = allbookings

	bookings_all = allbookings_of_dates.values('employee__id','employee__emp_name')
	bookings_confirmed = allbookings_of_dates.filter( booking_status="confirmed").values('employee__id'\
		,'employee__emp_name')
	bookings_pending = allbookings_of_dates.filter( booking_status="pending").values('employee__id'\
		,'employee__emp_name')
	bookings_cancelled = allbookings_of_dates.filter( booking_status="cancelled").values('employee__id'\
		,'employee__emp_name')
	
	reports = []
	reports_summary = dict()
	if index == "count" :
		bookings_all = bookings_all.annotate(booking_count=Count('employee__id')).order_by('-booking_count')
		bookings_confirmed = bookings_confirmed.annotate(booking_count=Count('employee__id'))
		bookings_pending = bookings_pending.annotate(booking_count=Count('employee__id'))
		bookings_cancelled = bookings_cancelled.annotate(booking_count=Count('employee__id'))
		for booking in bookings_all.iterator():
			report = dict()
			emp_name = booking['employee__emp_name'] 
			report["employee_name"] = emp_name
			report["all"] = booking['booking_count'] 
			#get booking_count for bookings_confirmed for the employeename, if not set it to zero.
			report["confirmed"] = getbookingcount_employee( bookings_confirmed, emp_name )
			report["pending"] = getbookingcount_employee( bookings_pending, emp_name )
			report["cancelled"] = getbookingcount_employee( bookings_cancelled, emp_name )
			reports.append(report)
	else : 
		bookings_all = bookings_all.annotate(booking_amount=Sum('booking_total')).order_by('-booking_amount')
		bookings_confirmed = bookings_confirmed.annotate(booking_amount=Sum('booking_total'))
		bookings_pending = bookings_pending.annotate(booking_amount=Sum('booking_total'))
		bookings_cancelled = bookings_cancelled.annotate(booking_amount=Sum('booking_total'))
		for booking in bookings_all.iterator():
			report = dict()
			emp_name = booking['employee__emp_name'] 
			report["employee_name"] = emp_name
			report["all"] =   round(float(booking['booking_amount']),2)
			#get booking_count for bookings_confirmed for the employeename, if not set it to zero.
			report["confirmed"] = getbookingtotal_employee( bookings_confirmed, emp_name )
			report["pending"] = getbookingtotal_employee( bookings_pending, emp_name )
			report["cancelled"] = getbookingtotal_employee( bookings_cancelled, emp_name )
			reports.append(report)
	reports_summary["bookings"] = reports
	# pdb.set_trace()
	reports_summary["graph"] = graph(reports)
	return  HttpResponse(json.dumps({"reports" :reports_summary }), content_type='application/json') 

def getbookingcount_employee( bookings, emp_name ):
	for booking in bookings.iterator():
		emp_name_booked = booking['employee__emp_name'] 
		if emp_name == emp_name_booked :
			return booking['booking_count'] 

	return 0

def getbookingtotal_employee( bookings, emp_name ):
	for booking in bookings.iterator():
		emp_name_booked = booking['employee__emp_name'] 
		if emp_name == emp_name_booked :
			return round(float(booking['booking_amount']),2) 

	return 0

def getbookingcount_service( bookings, service_name ):
	for booking in bookings.iterator():
		service_name_booked = booking['service__service_name'] 
		if service_name == service_name_booked :
			return booking['booking_count'] 

	return 0

def getbookingtotal_service( bookings, service_name ):
	for booking in bookings.iterator():
		service_name_booked = booking['service__service_name'] 
		if service_name == service_name_booked :
			return round(float(booking['booking_amount']),2) 

	return 0

def validate_date(d):
    try:
        datetime.strptime(d, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def graph(results):
	chartdata,emplist, allbk, confirmed, pending, cancelled = [],[],[],[],[],[]
	allbk.append("All Booking")
	confirmed.append("confirmed")
	pending.append("pending")
	cancelled.append("cancelled")
	emplist.append("Booking Details")

	for result in results:
		emplist.append(result["employee_name"])
		allbk.append(result["all"])
		confirmed.append(result["confirmed"])
		pending.append(result["pending"])
		cancelled.append(result["cancelled"])
	 
	chartdata.append( emplist )
	chartdata.append( allbk )
	chartdata.append( confirmed )
	chartdata.append( pending )
	chartdata.append( cancelled )
	return chartdata

def graph_service_data(results):
	chartdata,emplist, allbk, confirmed, pending, cancelled = [],[],[],[],[],[]
	allbk.append("All Booking")
	confirmed.append("confirmed")
	pending.append("pending")
	cancelled.append("cancelled")
	emplist.append("Booking Details")

	for result in results:
		emplist.append(result["service_name"])
		allbk.append(result["all"])
		confirmed.append(result["confirmed"])
		pending.append(result["pending"])
		cancelled.append(result["cancelled"])
	 
	chartdata.append( emplist )
	chartdata.append( allbk )
	chartdata.append( confirmed )
	chartdata.append( pending )
	chartdata.append( cancelled )
	return chartdata