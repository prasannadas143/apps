from twilio.rest import Client
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from appointmentscheduler.models import AppschedulerOptions
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.core import serializers
from PIL import Image
import io
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.forms.models import model_to_dict

def update_value(field_id, tab_id, newstep):
   item = AppschedulerOptions.objects.get(tab_id=int(tab_id), key = field_id)
   item.value = newstep;
   print(newstep);
   item.save()



@csrf_exempt
def SendSMSDyncamic(MobileNumber,Message):
	toNumber = MobileNumber
	print(toNumber);
	Message = Message
	print(Message);
	tab_id = 101;
	item = AppschedulerOptions.objects.filter(tab_id=tab_id)
	TWILIO_ACCOUNT_SID = item[0].value;
	print(TWILIO_ACCOUNT_SID);
	TWILIO_AUTH_TOKEN = item[1].value;
	print(TWILIO_AUTH_TOKEN);
	TWILIO_FROM_NUMBER = item[2].value;
	print(TWILIO_FROM_NUMBER);
	client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
	result=	client.api.account.messages.create(to=toNumber,	from_=TWILIO_FROM_NUMBER,body=Message)
	print(result);
	return HttpResponse(status=200)   

@csrf_exempt
def SendSMS(request):
	toNumber = request.POST['MobileNumber']
	print(toNumber);
	Message = request.POST['Message']
	print(Message);
	tab_id = 101;
	item = AppschedulerOptions.objects.filter(tab_id=tab_id)
	TWILIO_ACCOUNT_SID = item[0].value;
	print(TWILIO_ACCOUNT_SID);
	TWILIO_AUTH_TOKEN = item[1].value;
	print(TWILIO_AUTH_TOKEN);
	TWILIO_FROM_NUMBER = item[2].value;
	print(TWILIO_FROM_NUMBER);
	pdb.set_trace();
	client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
	result=	client.api.account.messages.create(to=toNumber,	from_=TWILIO_FROM_NUMBER,body=Message)
	print(result);
	pdb.set_trace();
	return HttpResponse(status=200)

@csrf_exempt
def SMSConfig(request):
	pdb.set_trace();
	tab_id = 101;
	message=None
	Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)
	SMSConfigdata = dict()
	
	if request.method == 'POST':
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(field, tab_id , newstep.strip() )

	item = AppschedulerOptions.objects.filter(tab_id=tab_id)
	o_TWILIO_ACCOUNT_SID = item[0].value;
	o_TWILIO_AUTH_TOKEN = item[1].value;
	o_TWILIO_FROM_NUMBER = item[2].value;

	items = {
	"o_TWILIO_ACCOUNT_SID":o_TWILIO_ACCOUNT_SID,
	"o_TWILIO_AUTH_TOKEN":o_TWILIO_AUTH_TOKEN,
    "o_TWILIO_FROM_NUMBER":o_TWILIO_FROM_NUMBER
	}
	SMSConfigdata['items'] = items
	# Then, do a redirect for example
	template_name="SMSConfig.html"
	templatename=  os.path.join('Options','SMS',template_name)
	return render(request,templatename, SMSConfigdata)