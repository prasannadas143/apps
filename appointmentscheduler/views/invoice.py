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
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@requires_csrf_token
def list_invoices(request):
	user_timezone = request.session['visitor_timezone']
	invoice_lists = AppschedulerInvoice.objects.all()
	invoices = []
	for invoice in  reversed(list(invoice_lists)):
		invoicedetails = dict()
		bkid = invoice.booking.id
		booking_instance = AppschedulerBookings.objects.filter(id=bkid)[0]
		invoicedetails['id'] = bkid
		invoicedetails['invoiceid'] = invoice.invoiceid
		invoicedetails['created'] = booking_instance.created.astimezone(pytz.timezone(user_timezone[0])).strftime( "%Y-%m-%d" )
		invoicedetails['duedate'] = booking_instance.created.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d %I:%M %p")
		invoicedetails['issued'] = booking_instance.date.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d ")
		invoicedetails['status'] =  booking_instance.booking_status
		invoicedetails['total'] =  round(float(booking_instance.booking_total),2)
		invoices.append( invoicedetails )
	# pdb.set_trace()
	return HttpResponse(json.dumps({"data" :invoices }), content_type='application/json') 
@requires_csrf_token
def generate_invoice(request,id):
	template_name = "invoice.html"
	user_timezone = request.session['visitor_timezone']
	invoicedetails =getinvoicedetails(  id, user_timezone)
	invoicedetails['id'] = id
	return render(request, template_name, invoicedetails)

@ensure_csrf_cookie
def delete_invoice(request,id=None):
    ainvoice=AppschedulerInvoice.objects.get( id=int(id) )
    ainvoice.delete()
    return HttpResponse(status=204)


@ensure_csrf_cookie
def delete_invoices(request):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        ainvoice=AppschedulerInvoice.objects.get(id=int( id ) )
        ainvoice.delete()
    return HttpResponse(status=204)

@ensure_csrf_cookie
def print_invoice_pdf(request,id):
	template_name = "invoice.html"
	user_timezone = request.session['visitor_timezone']
	result = BytesIO()
	invoicedetails =getinvoicedetails(  id, user_timezone)
	# if getpdf:
	v_country ="califarnia"
	v_add1 =  "sunnyvale"
	v_add2 = "home tree"
	v_zip = "2344455"
	v_country_abbr = "cl"
	v_phone = "+91992888377"
	v_email = "ggggd@hhhh.com"
	v_website = "sddff@hjjjs.com"
	 
	vendor_address = {
	"v_country" : v_country,
	"v_add1" : v_add1,
	"v_add2" : v_add2,
	"v_zip" : v_zip,
	"v_country_abbr" : v_country_abbr,
	"v_phone" : v_phone,
	"v_email" : v_email,
	"v_website" : v_website
	}
	file = "invoice_{0}.pdf".format(id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="{}"'.format(file)

	buffer = BytesIO()
	invoice_pdf = canvas.Canvas(buffer,  pagesize=letter)
	invoice_pdf.setTitle(file)
	invoice_pdf = createinvoicepdf(invoice_pdf, invoicedetails, vendor_address)
	invoice_pdf.showPage()
	invoice_pdf.save()

	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)

	return response


def createinvoicepdf(canvas , invoicedetails, vendor_address):
	canvas.setLineWidth(.3)
	canvas.setFont('Helvetica', 12)
	c_address = invoicedetails['c_add1'] + "  " + invoicedetails['c_add1'] 


	canvas.drawString(275,725,'Invoice No:')
	canvas.drawString(340	,725,str(invoicedetails['invoiceno']))
	canvas.drawString(275,710,'Date:')
	canvas.drawString(320	,710,str(invoicedetails['issued']))
	pos_x = 120
	pos_y = 645	
	end_pos_x = pos_x + 470

	canvas.line(pos_x,pos_y,end_pos_x,pos_y)
	pos_y+=5
	canvas.drawString(pos_x, pos_y,"Bill To:")
	pos_y-=30
	canvas.drawString(pos_x,pos_y, invoicedetails['c_name'])
	pos_y-=15
	canvas.drawString(pos_x,pos_y, c_address)
	pos_y-=15
	canvas.drawString(pos_x,pos_y, invoicedetails['country'] + "   " + invoicedetails['c_zip']) 
	pos_y-=15
	canvas.drawString(pos_x,pos_y,"Phone:" + "  " + invoicedetails['c_phone'] + " " + "Fax:")					
						
	pos_y-=55			
	canvas.drawString(340, pos_y, "Invoice")
	pos_y-= 10
	canvas.line(pos_x,pos_y,end_pos_x,pos_y)
	pos_y-= 15

	canvas.drawString(pos_x,pos_y,"Description")
	str_pos_x1 = pos_x+220	
	canvas.drawString( str_pos_x1,pos_y,"Price" )	
	str_pos_x2 = pos_x+420	

	canvas.drawString(str_pos_x2,pos_y, "Amount")	
	pos_y-= 10
	canvas.line(pos_x,pos_y,end_pos_x,pos_y)
	pos_y-= 15

	canvas.drawString(pos_x,pos_y,invoicedetails['servicename'])	
	canvas.drawString(str_pos_x1,pos_y,str(invoicedetails['price']))	
	canvas.drawString( str_pos_x2,pos_y,str(invoicedetails['total']))	
	sub_x= str_pos_x1 + 130
	pos_y-= 40
	canvas.drawString(pos_x,pos_y,"Note:")	
	canvas.drawString(sub_x,pos_y,"SubTotal:")	
	x_val = str_pos_x2 - 10
	canvas.drawString(x_val,pos_y,str(invoicedetails['price']))	

	Discount_x = str_pos_x1 + 130
	pos_y-= 15
	canvas.drawString(pos_x,pos_y,"Thanks for your Best wishes:")	
	canvas.drawString(Discount_x,pos_y,"Discount:")	
	canvas.drawString(x_val,pos_y,str(invoicedetails['discount']))	

	Total_x = str_pos_x1 + 150
	pos_y-= 15
	canvas.drawString(Total_x,pos_y,"Total:")	
	canvas.drawString(x_val,pos_y,str(invoicedetails['total']))	

	Deposit_x = str_pos_x1 + 140
	pos_y-= 15	
	canvas.drawString(Deposit_x,pos_y,"Deposit:")
	canvas.drawString(x_val,pos_y,str(invoicedetails['deposit']))	
		
	amoount_due = str_pos_x1 + 110
	pos_y-= 15	
	canvas.drawString(amoount_due,pos_y,"Amount Due:")	
	canvas.drawString(x_val,pos_y,str(invoicedetails['amount_due']))	
	 
	pos_y-= 50	

	canvas.drawString(pos_x,pos_y,vendor_address['v_country'])
	pos_y-= 10	
	canvas.line(pos_x,pos_y,end_pos_x,pos_y)
	pos_y-= 15	
	canvas.drawString(pos_x,pos_y,vendor_address['v_add1'])
	v_pos_x = pos_x + 150
	canvas.drawString(v_pos_x,pos_y,"phone:" + "  " + vendor_address['v_phone'])
	pos_y-= 15	
	canvas.drawString(pos_x,pos_y,vendor_address['v_add2'])
	canvas.drawString(v_pos_x,pos_y,"Email:" +  "  " + vendor_address['v_email'])
	pos_y-= 15	
	canvas.drawString(pos_x,pos_y,vendor_address['v_country_abbr'] + "  " + vendor_address['v_zip']) 
	canvas.drawString(v_pos_x,pos_y,"Website:" +  "  " + vendor_address['v_website'])
	pos_y-= 10	
	canvas.line(pos_x,pos_y,end_pos_x,pos_y)

	return canvas

def getinvoicedetails(id, user_timezone):
	invoicedetails = dict()
	invoice_instance = AppschedulerBookings.objects.filter(id=id)[0]
	invoicedetails['c_name'] = invoice_instance.c_name 
	invoicedetails['country'] = invoice_instance.country 
	invoicedetails['c_city'] = invoice_instance.c_city 
	invoicedetails['c_state'] = invoice_instance.c_state 
	invoicedetails['c_zip'] = invoice_instance.c_zip 
	invoicedetails['c_add1'] = invoice_instance.c_address_1 
	invoicedetails['c_add2'] = invoice_instance.c_address_2
	invoicedetails['c_phone'] = str(invoice_instance.c_phone) 

	# todaydate= datetime.now().strftime("%Y-%m-%d")
	# bookingdetails["defaultdate"] = todaydate 
	# bookingdetails["customer_fields"] = customer_fields
	invoice_obj = AppschedulerInvoice.objects.filter(booking = invoice_instance)
	if not invoice_obj.count():
		ctc_bookingid = invoice_instance.bookingid
		in_id = int(ctc_bookingid[-12:]) 
		invoiceid = ctc_bookingid[:-12] + str(in_id)
		invoice_obj = AppschedulerInvoice.objects.create(booking = invoice_instance, invoiceid= invoiceid)
		invoice_no = invoice_obj.id

	else:
		invoiceid = invoice_obj[0].invoiceid
		invoice_no = invoice_obj[0].id

	invoicedetails['invoiceid'] = invoiceid
	invoicedetails['invoiceno'] = invoice_no
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

	for key,value in invoicedetails.items():
		if value is None:
			invoicedetails[key] =''

	return invoicedetails