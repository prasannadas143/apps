from twilio.rest import Client
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import pdb,os,json,re,pytz
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie,csrf_exempt
import configparser
from django.conf import settings
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from appointmentscheduler.models import  SmsSentStatus
from shoppingcart.options.models import  Options


config = configparser.ConfigParser()
config.read(settings.DOTENV_FILE)

def update_value(tab_id, field, newstep):
   item = get_object_or_404( Options,  tab_id=int(tab_id), key = field )
   item.value = newstep;
   item.save()

@csrf_exempt
def SendMail(request):
	tab_id = 5;
	items = Options.objects.filter(tab_id=tab_id).values('key', 'value')
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



@csrf_exempt
def EmailConfig(request):
	tab_id = 5;
	message=None
	# use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)
	EmailConfigdata = dict()

	if request.method == 'POST':
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(tab_id , field.strip() , newstep.strip())

	items = Options.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item
	flag = None
	o_FromEmail = items_dict['o_FromEmail']['value']
	o_FromEmailPassword = items_dict['o_FromEmailPassword']['value']
	if config['DEFAULT']['EMAIL_HOST_USER'] != o_FromEmail :
		config.set('DEFAULT','EMAIL_HOST_USER',o_FromEmail)
		flag = 1
	if config['DEFAULT']['EMAIL_HOST_PASSWORD'] != o_FromEmailPassword :
		config.set('DEFAULT','EMAIL_HOST_PASSWORD',o_FromEmailPassword)
		flag = 1
	# Writing our configuration file to 'example.cfg'
	if flag :
		with open(settings.DOTENV_FILE, 'w') as configfile:
		    config.write(configfile)
	items = {
	"o_FromEmail":o_FromEmail,
	"o_FromEmailPassword":o_FromEmailPassword
	}

	EmailConfigdata['items'] = items

	# Then, do a redirect for example
	templatename="EmailNotification.html"
	return render(request,templatename, EmailConfigdata)





@ensure_csrf_cookie
def SendSMS(request):
	toNumber = request.POST['MobileNumber']
	print(toNumber);
	Message = request.POST['Message']
	print(Message);
	tab_id = 101;
	items = Options.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item

	TWILIO_ACCOUNT_SID =  items_dict['o_TWILIO_ACCOUNT_SID']['value']
	print(TWILIO_ACCOUNT_SID);
	TWILIO_AUTH_TOKEN =  items_dict['o_TWILIO_AUTH_TOKEN']['value']
	print(TWILIO_AUTH_TOKEN);
	TWILIO_FROM_NUMBER =  items_dict['o_TWILIO_FROM_NUMBER']['value']
	client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
	result=	client.api.account.messages.create(to=toNumber,	from_=TWILIO_FROM_NUMBER,body=Message)
	print(result);
	return HttpResponse(status=200)

@requires_csrf_token
def SMSConfig(request):
	tab_id = 101;
	message=None
	options  = Options.objects.all() # use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)
	SMSConfigdata = dict()
	
	if request.method == 'POST':
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			if field.strip()!= "csrfmiddlewaretoken":
				update_value(field, tab_id , newstep.strip() )

	items = Options.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item

	TWILIO_ACCOUNT_SID =  items_dict['o_TWILIO_ACCOUNT_SID']['value']
	print(TWILIO_ACCOUNT_SID);
	TWILIO_AUTH_TOKEN =  items_dict['o_TWILIO_AUTH_TOKEN']['value']
	print(TWILIO_AUTH_TOKEN);
	TWILIO_FROM_NUMBER =  items_dict['o_TWILIO_FROM_NUMBER']['value']
	items = {
	"o_TWILIO_ACCOUNT_SID": TWILIO_ACCOUNT_SID,
	"o_TWILIO_AUTH_TOKEN": TWILIO_AUTH_TOKEN,
    "o_TWILIO_FROM_NUMBER": TWILIO_FROM_NUMBER
	}
	flag = None
	if config['DEFAULT']['TWILIO_ACCOUNT_SID'] != TWILIO_ACCOUNT_SID :
		config.set('DEFAULT','TWILIO_ACCOUNT_SID',TWILIO_ACCOUNT_SID)
		flag = 1
	if config['DEFAULT']['TWILIO_AUTH_TOKEN'] != TWILIO_AUTH_TOKEN :
		config.set('DEFAULT','TWILIO_AUTH_TOKEN',TWILIO_AUTH_TOKEN)
		flag = 1
	if config['DEFAULT']['TWILIO_FROM_NUMBER'] != TWILIO_FROM_NUMBER :
		config.set('DEFAULT','TWILIO_FROM_NUMBER',TWILIO_FROM_NUMBER)
		flag = 1	
	# Writing our configuration file to 'example.cfg'
	if flag :
		with open(settings.DOTENV_FILE, 'w') as configfile:
		    config.write(configfile)
	SMSConfigdata['items'] = items
	
	# # Then, do a redirect for example
	# SMSConfigdata['smsdetails'] = smsinstances

	templatename="SMSConfig.html"
	return render(request,templatename, SMSConfigdata)

@ensure_csrf_cookie
def listsms(request):
	#Display the Sms details
	user_timezone = request.session['visitor_timezone']
	smsinstances = SmsSentStatus.objects.filter(appname="appointmentscheduler")
	listsms=[]
	for smsinstance in smsinstances:
		data=dict()
		data['id'] = smsinstance.pk
		smsdatetime = smsinstance.sms_sent_time.astimezone(pytz.timezone(user_timezone[0]))
		format = '%Y-%m-%d %H:%M %p'
		data['sms_sent_time'] = smsdatetime.strftime(format)
		data['phone_no'] = smsinstance.phone_no
		data['message'] = smsinstance.message
		data['status'] = smsinstance.status
		listsms.append(data)

	return  HttpResponse(json.dumps({"data" :listsms }), content_type='application/json')   

@ensure_csrf_cookie
def deletesms(request,id=None):
    """ Delete booking """

    # smsobj = get_object_or_404( SmsSentStatus,  pk=int(id) )
    # smsobj.delete()
    # pdb.set_trace()
    return  HttpResponse(status=204)   

@ensure_csrf_cookie
def deletemultiplesms(request):
    """ Delete list of booking """

    # deleteids= request.POST['rowids']	
    # for id in deleteids.split(",") :
    #     smsobj=get_object_or_404( SmsSentStatus,  pk=int(id) )
    #     smsobj.delete()

    return  HttpResponse(status=204)   

