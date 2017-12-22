from django.shortcuts import  render, HttpResponse,get_object_or_404
import json
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from appointmentscheduler.models  import AppschedulerBookings,AppschedulerInvoice,AppschedulerOptions
import pytz
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from twilio.rest import Client
import html
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from appointmentscheduler.views.Options.Editor import ckEditor

@requires_csrf_token
def list_invoices(request):
	user_timezone = request.session['visitor_timezone'] 
	# import pdb
	# pdb.set_trace()
	invoice_lists = AppschedulerInvoice.objects.order_by('-id').select_related('booking').values("booking__id", "invoiceid",\
	 "booking__created",	"booking__date",  "booking__booking_status", "booking__booking_total")
	invoices = []
	for invoice in  invoice_lists.iterator():
		invoicedetails = dict()
		invoicedetails['id'] = invoice['booking__id']
		invoicedetails['invoiceid'] = invoice['invoiceid']
		invoicedetails['created'] = booking_instance['booking__created'].astimezone(pytz.timezone(user_timezone[0])).strftime( "%Y-%m-%d" )
		invoicedetails['duedate'] = booking_instance['booking__created'].astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d %I:%M %p")
		invoicedetails['issued'] = booking_instance['booking__date'].astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d ")
		invoicedetails['status'] =  booking_instance['booking__booking_status']
		invoicedetails['total'] =  round(float(booking_instance['booking__booking_total']),2)
		invoices.append( invoicedetails )

	# pdb.set_trace()
	return HttpResponse(json.dumps({"data" :invoices }), content_type='application/json') 
@requires_csrf_token
def generate_invoice(request,id):
	template_name = "invoice.html"
	user_timezone = request.session['visitor_timezone']
	invoicedetails =getinvoicedetails(  id, user_timezone)
	locals().update(invoicedetails)
	opertype="InvoiceEmail"
	tmpdtls=ckEditor.GetTemplateDetailByTemplateID(opertype)
	if tmpdtls :
		emailres = tmpdtls.DesignedTemplate
		subject_email = tmpdtls.subject

	else :
		subject_email = opertype

		emailres =" customername {customer_name} bookingid {bookingid} date {service_start_time} day {issued}"
	opertype="InvoiceSMS"
	tmpdtls=ckEditor.GetTemplateDetailByTemplateID(opertype)
	if tmpdtls :
		smstmpdtls = tmpdtls.DesignedTemplate
		subject_sms = tmpdtls.subject
	else :
		subject_sms = opertype
		smstmpdtls =" customername {customer_name} bookingid {bookingid} date {service_start_time} day {issued}"

	booking = get_object_or_404( AppschedulerBookings,  pk=int(id) )
	duration =  booking.service.total 
	servicedesc =  booking.service.service_desc
	empname = booking.employee.emp_name
	getstarttime = booking.service_start_time.astimezone(booking.time_zone)
	format = '%Y-%m-%d %H:%M %p'
	service_start_time = getstarttime.strftime(format)
	getendtime = booking.service_end_time.astimezone(booking.time_zone)
	service_end_time = getendtime.strftime(format)
	tab_id = 5

	customeremail = booking.c_email
	employeeemail = booking.employee.emp_name
	customernumber = str(booking.c_phone)
	employeenumber = str(booking.employee.phone)
	emailbody = emailres.format(**locals())
	smsbody = smstmpdtls.format(**locals())
	# pdb.set_trace()
	dtls ={ "invoicedetails" : invoicedetails,
					  "emailbody" : emailbody,
					  "subject_email" : subject_email,
					  "smsbody" : smsbody,
					  "bookingpk" : booking.id 
					}
	return render(request, template_name, dtls)

@ensure_csrf_cookie
def sendmail_invoice(request):
	if request.method == "POST":
		bookingpk = request.POST["bookingpk"]
		subjectmail = request.POST["subjectmail"]
		emailbody = request.POST["mailcontent"]
		tab_id = 5
		item = AppschedulerOptions.objects.filter(tab_id=tab_id)
		fromaddr = item[0].value
		o_FromEmailPassword = item[1].value
		booking = get_object_or_404( AppschedulerBookings,  pk=int(bookingpk) )
		toaddr = booking.c_email
		empemail = booking.employee.email
		emailbody = html.unescape(emailbody)

		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr + "," + empemail
		msg['Subject']  = subjectmail
		# msg.add_header('Content-Type','text/html')
		msg.attach(MIMEText(emailbody, 'html'))
		try:

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login(fromaddr, o_FromEmailPassword)
			message = msg.as_string()
			print(fromaddr);
			print(toaddr);
			server.sendmail(fromaddr, toaddr, message)
			server.quit()  
		except:
  			print("There was an error sending the email. Check the smtp settings.")	
	return HttpResponse(status=204)

@ensure_csrf_cookie
def sendmsg_invoice(request):
	if request.method == "POST":
		bookingpk = request.POST["bookingpk"]
		msgbody = request.POST["msgcontent"]
		booking = get_object_or_404( AppschedulerBookings,  pk=int(bookingpk) )
		toNumber = str(booking.c_phone)

		tab_id = 101;
		item = AppschedulerOptions.objects.filter(tab_id=tab_id)
		TWILIO_ACCOUNT_SID = item[0].value;
		print(TWILIO_ACCOUNT_SID);
		TWILIO_AUTH_TOKEN = item[1].value;
		print(TWILIO_AUTH_TOKEN);
		TWILIO_FROM_NUMBER = item[2].value;
		print(TWILIO_FROM_NUMBER);
		try:
			client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
			result= client.api.account.messages.create(to=toNumber, from_=TWILIO_FROM_NUMBER,body=msgbody)
			print(result)
		except:
			print("There was an error sending the sms. Check the message settings.")	

	return HttpResponse(status=204)	

@ensure_csrf_cookie
def delete_invoice(request,id=None):
    ainvoice=  get_object_or_404( AppschedulerInvoice,  pk=int(id) )
    ainvoice.delete()
    return HttpResponse(status=204)


@ensure_csrf_cookie
def delete_invoices(request):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        ainvoice=get_object_or_404( AppschedulerInvoice,  pk=int(id) )
        ainvoice.delete()
    return HttpResponse(status=204)

@ensure_csrf_cookie
def print_invoice_pdf(request,id):
	template_name = "invoice.html"
	user_timezone = request.session['visitor_timezone']
	result = BytesIO()
	invoicedetails =getinvoicedetails(  id, user_timezone)
	# if getpdf:
	# v_country ="califarnia"
	# v_add1 =  "sunnyvale"
	# v_add2 = "home tree"
	# v_zip = "2344455"
	# v_country_abbr = "cl"
	# v_phone = "+91992888377"
	# v_email = "ggggd@hhhh.com"
	# v_website = "sddff@hjjjs.com"
	 
	# vendor_address = {
	# "v_country" : v_country,
	# "v_add1" : v_add1,
	# "v_add2" : v_add2,
	# "v_zip" : v_zip,
	# "v_country_abbr" : v_country_abbr,
	# "v_phone" : v_phone,
	# "v_email" : v_email,
	# "v_website" : v_website
	# }
	vendor_address= Invoice.GetInvoiceCompanyvalues()
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
	c_address = invoicedetails['add1'] + "  " + invoicedetails['add1'] 


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
	canvas.drawString(pos_x,pos_y, invoicedetails['name'])
	pos_y-=15
	canvas.drawString(pos_x,pos_y, c_address)
	pos_y-=15
	canvas.drawString(pos_x,pos_y, invoicedetails['country'] + "   " + invoicedetails['zip']) 
	pos_y-=15
	canvas.drawString(pos_x,pos_y,"Phone:" + "  " + invoicedetails['phone'] + " " + "Fax:")					
						
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

	canvas.drawString(pos_x,pos_y,invoicedetails['service'])	
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
	invoice_instance = get_object_or_404( AppschedulerBookings,  pk=int(id) )
	invoicedetails['id'] = id
	invoicedetails['customer_name'] = invoice_instance.c_name 
	if invoice_instance.country is not None:
		invoicedetails['country'] = invoice_instance.country.CountryName
	invoicedetails['city'] = invoice_instance.c_city 
	invoicedetails['state'] = invoice_instance.c_state 
	invoicedetails['zip'] = invoice_instance.c_zip 
	invoicedetails['add1'] = invoice_instance.c_address_1 
	invoicedetails['add2'] = invoice_instance.c_address_2
	invoicedetails['phone'] = str(invoice_instance.c_phone) 
	invoicedetails['ip'] = invoice_instance.ip
	invoicedetails['c_name'] = invoice_instance.c_name
	invoicedetails['c_email'] = invoice_instance.c_email

	# todaydate= datetime.now().strftime("%Y-%m-%d")
	# bookingdetails["defaultdate"] = todaydate 
	# bookingdetails["customer_fields"] = customer_fields
	invoice_obj = AppschedulerInvoice.objects.filter(booking = invoice_instance)
	if not invoice_obj.exists():
		ctc_bookingid = invoice_instance.bookingid
		in_id = int(ctc_bookingid[-12:]) 
		invoiceid = ctc_bookingid[:-12] + str(in_id)
		invoice_obj = AppschedulerInvoice.objects.create(booking = invoice_instance, invoiceid= invoiceid)
		invoice_no = invoice_obj.id

	else:
		invoiceid = invoice_obj[0].invoiceid
		invoice_no = invoice_obj[0].id

	invoicedetails['invoice_id'] = invoiceid
	invoicedetails['invoiceno'] = invoice_no
	invoicedetails['bookingid'] = invoice_instance.bookingid
	invoicedetails['created'] = invoice_instance.created.astimezone(pytz.timezone(user_timezone[0])).strftime( "%Y-%m-%d" )
	invoicedetails['duedate'] = invoice_instance.created.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d %I:%M %p")
	invoicedetails['issued'] = invoice_instance.date.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d ")
	invoicedetails['booking_status'] =  invoice_instance.booking_status
	invoicedetails['service'] =  invoice_instance.service.service_name
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