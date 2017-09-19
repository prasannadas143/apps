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
from datetime import datetime
from pytz import country_timezones, timezone
from tzlocal import get_localzone
import re,pytz,calendar
from datetime import datetime, timedelta
import dateutil.parser as dparser
from copy import deepcopy

@requires_csrf_token
def generate_invoice(request,id):
	template_name = "invoice.html"
	invoicedetails = dict()
	invoice_instance = AppschedulerBookings.objects.filter(id=id)[0]
	user_timezone = request.session['visitor_timezone']
	invoicedetails['bookingdetails'] = invoice_instance 
	# todaydate= datetime.now().strftime("%Y-%m-%d")
	# bookingdetails["defaultdate"] = todaydate 
	# bookingdetails["customer_fields"] = customer_fields
	invoice_obj = AppschedulerInvoice.objects.filter(booking = invoice_instance)
	if not invoice_obj.count():
		ctc_bookingid = invoice_instance.bookingid
		in_id = int(ctc_bookingid[-12:]) 
		invoiceid = ctc_bookingid[:-12] + str(in_id)
		invoice_obj = AppschedulerInvoice.objects.create(booking = invoice_instance, invoiceid= invoiceid)

	invoicedetails['created'] = invoice_instance.created.astimezone(pytz.timezone(user_timezone[0])).strftime( "%Y-%m-%d" )
	invoicedetails['duedate'] = invoice_instance.created.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d %I:%M %p")
	invoicedetails['issued'] = invoice_instance.date.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d ")
	invoicedetails['status'] =  invoice_instance.booking_status
	invoicedetails['servicename'] =  invoice_instance.service.service_name
	invoicedetails['price'] =  round(float(invoice_instance.booking_price),2)

	invoicedetails['total'] =  round(float(invoice_instance.booking_total),2)
	invoicedetails['deposit'] =  round(float(invoice_instance.booking_deposit),2)
	invoicedetails['discount'] =  0
	invoicedetails['tax'] =  round(float(invoice_instance.booking_tax),2)
	invoicedetails['amount_due'] =  round(float(invoicedetails['total']) - float(invoicedetails['deposit']) - float(invoicedetails['discount']),2)
	if invoicedetails['amount_due'] < 0:
		invoicedetails['amount_due'] = 0
	invoicedetails['c_notes'] = invoice_instance.c_notes
	return render(request, template_name, invoicedetails)
