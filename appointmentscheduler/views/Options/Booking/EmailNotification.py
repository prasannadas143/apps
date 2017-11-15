import os
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render, get_object_or_404
from appointmentscheduler.models import AppschedulerOptions
from django.views.decorators.csrf import  csrf_exempt
import pdb,os
from django.http import HttpResponse
from appointmentscheduler.views.Options.Editor import ckEditor
from appointmentscheduler.models import AppschedulerBookings


@csrf_exempt
def SendMail(request):
	tab_id = 5;
	items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item

	o_FromEmail = items_dict['o_FromEmail']['value']
	o_FromEmailPassword = items_dict['o_FromEmailPassword']['value']
	if request.method == 'POST':

		fromaddr = o_FromEmail
		toaddr = request.POST['EmailAddress']
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject']  = request.POST['Subject']
		body =  request.POST['Body']
		# msg['EMAIL_USE_TLS'] = True
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, o_FromEmailPassword)
		text = msg.as_string()
		print(fromaddr);
		print(toaddr);
		print(text);
		server.sendmail(fromaddr, toaddr, text)
		server.quit()						
		return HttpResponse(status=200)
	else :

		items = {
		"o_FromEmail":o_FromEmail,
		"o_FromEmailPassword":o_FromEmailPassword
		}
		EmailConfigdata = dict()
		EmailConfigdata['items'] = items
		template_name="EmailNotification.html"
		templatename=  os.path.join('Options','Booking',template_name)
		return render(request,templatename, EmailConfigdata)


def update_value(field_id, tab_id, newstep):
   item = get_object_or_404( AppschedulerOptions,  tab_id=int(tab_id), id = int(field_id) )
   item.value = newstep;
   item.save()

@csrf_exempt
def SaveMailSettings(request):
	tab_id = 5;
	message=None
	# use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)
	EmailConfigdata = dict()
	if request.method == 'POST':
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(field, tab_id , newstep.strip() )

	items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item

	o_FromEmail = items_dict['o_FromEmail']['value']
	o_FromEmailPassword = items_dict['o_FromEmailPassword']['value']
	items = {
	"o_FromEmail":o_FromEmail,
	"o_FromEmailPassword":o_FromEmailPassword
	}
	EmailConfigdata['items'] = items

	# Then, do a redirect for example
	template_name="EmailNotification.html"
	templatename=  os.path.join('Options','Booking',template_name)
	return render(request,templatename, EmailConfigdata)


def SendMailFromBooking(bookingid):
	templateid = 2
	tmpdtls=ckEditor.GetTemplateDetailByTemplateID(templateid)
	emailres = tmpdtls.DesignedTemplate
	Subject = tmpdtls.subject

	tab_id = 5
	items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item

	o_FromEmail = items_dict['o_FromEmail']['value']
	o_FromEmailPassword = items_dict['o_FromEmailPassword']['value']
	booking =  get_object_or_404( AppschedulerBookings, id = bookingid )
	customer_name = booking.c_name
	bookingid = booking.bookingid
	date = booking.service_start_time.astimezone(booking.time_zone).strftime( "%I:%M %p" )
	day = booking.date.astimezone(booking.time_zone).strftime("%Y-%m-%d")
	toaddr = booking.c_email

	fromaddr = o_FromEmail
	emailbody = emailres.format(Name=customer_name,bookingID=bookingid, date=date,Day=day)

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject']  = Subject
	# msg['EMAIL_USE_TLS'] = True
	print(fromaddr);
	print(o_FromEmailPassword);
	print(Subject);
	print(emailbody);
	msg.attach(MIMEText(emailbody, "html"))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(fromaddr, o_FromEmailPassword)
	text = msg.as_string()
	print(fromaddr);
	print(toaddr);
	server.sendmail(fromaddr, toaddr, text)
	server.quit()						
	return 