import os
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
import datetime, pdb
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from appointmentscheduler.models import AppschedulerOptions
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.core import serializers
import io
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.forms.models import model_to_dict
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

@csrf_exempt
def SendMail(request):
	tab_id = 5;
	if request.method == 'POST':
		item = AppschedulerOptions.objects.filter(tab_id=tab_id)
		o_FromEmail = item[0].value;
		o_FromEmailPassword = item[1].value;
		fromaddr = o_FromEmail
		toaddr = request.POST['EmailAddress']
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject']  = request.POST['Subject']
		body =  request.POST['Body']
		msg['EMAIL_USE_TLS'] = True
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
		template_name="EmailNotification.html"
		templatename=  os.path.join('Options','Booking',template_name)
		return render(request,templatename)


def update_value(field_id, tab_id, newstep):
   item = AppschedulerOptions.objects.get(tab_id=int(tab_id), key = field_id)
   item.value = newstep;
   item.save()

@csrf_exempt
def SaveMailSettings(request):
	tab_id = 5;
	message=None
	Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)
	EmailConfigdata = dict()
	if request.method == 'POST':
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(field, tab_id , newstep.strip() )

	item = AppschedulerOptions.objects.filter(tab_id=tab_id)
	o_FromEmail = item[0].value;
	o_FromEmailPassword = item[1].value;
	items = {
	"o_FromEmail":o_FromEmail,
	"o_FromEmailPassword":o_FromEmailPassword
	}
	EmailConfigdata['items'] = items

	# Then, do a redirect for example
	template_name="EmailNotification.html"
	templatename=  os.path.join('Options','Booking',template_name)
	return render(request,templatename, EmailConfigdata1)