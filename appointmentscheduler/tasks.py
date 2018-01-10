from __future__ import absolute_import
from celery.decorators import task
from celery import shared_task
import celery
from .models import SmsSentStatus
import smtplib,  pdb
from twilio.rest import Client
from celery.utils.log import get_task_logger
from celery.contrib import rdb
from datetime import datetime, date, time
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from appointmentscheduler.views.Options.Editor import ckEditor
from appointmentscheduler.models import AppschedulerBookings, AppschedulerOptions
from django.conf import settings
# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables

logger = get_task_logger(__name__)
# @shared_task
class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # rdb.set_trace()
        status = "Failed"
        created_time  = datetime.utcnow()
        msg_info = self.request.kwargs
        if 'email' in msg_info :
            toaddr =  msg_info['email']
            message = msg_info['emailcontent'] 
        if 'to_sms' in msg_info :
            tosms =  msg_info['to_sms']
            message = msg_info['smscontent'] 
            smssentstatus = SmsSentStatus(sms_sent_time=created_time ,phone_no=tosms ,message=message ,status=status)
            smssentstatus.save()
        
        logger.error('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        # rdb.set_trace()
        status = "Success"
        created_time  = datetime.utcnow()
        msg_info = self.request.kwargs
        if 'email' in msg_info :
            toaddr =  msg_info['email']
            message = msg_info['emailcontent'] 
        if 'to_sms' in msg_info :
            tosms =  msg_info['to_sms']
            message = msg_info['smscontent'] 
            smssentstatus = SmsSentStatus(sms_sent_time=created_time ,phone_no=tosms ,message=message ,status=status)
            smssentstatus.save()


@task(bind=True, base=MyTask, default_retry_delay=2)  
def send_sms(self,bookingid,opertype, *args, **kwargs):
    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        booking = AppschedulerBookings.objects.get(id=bookingid)
        templateid = 5
        opertype = opertype + "SMS"
        tmpdtls=ckEditor.GetTemplateDetailByTemplateID(opertype)
        if tmpdtls :
            smstmpdtls = tmpdtls.DesignedTemplate
            Subject = tmpdtls.subject
        else :
            Subject = opertype

            smstmpdtls =" customername {customer_name} bookingid {bookingid} date {service_start_time} day {issued}"
       
        customer_name = booking.c_name
        bookingid = booking.bookingid
        service_start_time = booking.service_start_time.astimezone(booking.time_zone).strftime( "%I:%M %p" )
        issued = booking.date.astimezone(booking.time_zone).strftime("%Y-%m-%d")
        service = booking.service.service_name
        duration =  booking.service.total 
        servicedesc =  booking.service.service_desc
        empname = booking.employee.emp_name
        getstarttime = booking.service_start_time.astimezone(booking.time_zone)
        format = '%Y-%m-%d %H:%M %p'
        service_start_time = getstarttime.strftime(format)
        getendtime = booking.service_start_time.astimezone(booking.time_zone)
        service_start_time = getendtime.strftime(format)
        service_price = booking.booking_price
        tax = booking.booking_tax
        total_price = booking.booking_total
        booking_deposit = booking.booking_deposit
        booking_status = booking.booking_status
      
        Message = smstmpdtls.format(**locals())
        toNumber = str(booking.c_phone)
        print(toNumber);
      
        TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
        print(TWILIO_ACCOUNT_SID);
        TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
        print(TWILIO_AUTH_TOKEN);
        TWILIO_FROM_NUMBER = settings.TWILIO_FROM_NUMBER
        print(TWILIO_FROM_NUMBER);
        # rdb.set_trace()  # <- set break-point
        self.request.kwargs['to_sms'] = toNumber
        self.request.kwargs['smscontent'] = Message
        client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
        result= client.api.account.messages.create(to=toNumber, from_=TWILIO_FROM_NUMBER,body=Message)
        print(result)


    except Exception as exc:
       # overrides the default delay to retry after 1 minute
        logger.error('Error while doing sending sms', exc_info=True)

        raise self.retry(exc=exc, max_retries=3)                 

    return 



# @shared_task
@task(bind=True, base=MyTask, default_retry_delay=2)  
def send_email( self,bookingid, opertype, *args, **kwargs):
    try:
        booking = AppschedulerBookings.objects.get(pk=bookingid)
        templateid = 2
        opertype = opertype + "EMAIL"
        tmpdtls=ckEditor.GetTemplateDetailByTemplateID(opertype)
        if tmpdtls :
            emailres = tmpdtls.DesignedTemplate
            Subject = tmpdtls.subject
        else :
            emailres =" customername {customer_name} bookingid {bookingid} date {service_start_time} day {issued}"
            Subject = opertype


        tab_id = 5
        item = AppschedulerOptions.objects.filter(tab_id=tab_id)
        o_FromEmail = item[0].value
        o_FromEmailPassword = item[1].value
        customer_name = booking.c_name
        bookingid = booking.bookingid
        service_start_time = booking.service_start_time.astimezone(booking.time_zone).strftime( "%I:%M %p" )
        issued = booking.date.astimezone(booking.time_zone).strftime("%Y-%m-%d")
        service = booking.service.service_name
        duration =  booking.service.total 
        servicedesc =  booking.service.service_desc
        empname = booking.employee.emp_name
        getstarttime = booking.service_start_time.astimezone(booking.time_zone)
        format = '%Y-%m-%d %H:%M %p'
        service_start_time = getstarttime.strftime(format)
        getendtime = booking.service_start_time.astimezone(booking.time_zone)
        service_start_time = getendtime.strftime(format)
        service_price = booking.booking_price
        tax = booking.booking_tax
        total_price = booking.booking_total
        booking_deposit = booking.booking_deposit
        booking_status = booking.booking_status
        toaddr = booking.c_email
        fromaddr = settings.DEFAULT_FROM_EMAIL
        o_FromEmailPassword = settings.EMAIL_HOST_PASSWORD
        emailbody = emailres.format(**locals())

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
        text = msg.as_string()
        self.request.kwargs['email'] = toaddr
        self.request.kwargs['emailcontent'] = text
        # rdb.set_trace()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(fromaddr, o_FromEmailPassword)
        print(fromaddr);
        print(toaddr);
        server.sendmail(fromaddr, toaddr, text)
        server.quit()   
   
    except Exception as exc:
        import traceback

       # overrides the default delay to retry after 1 minute
        logger.info('Error while doing sending email', exc_info=1)
        raise self.retry(exc=exc,  max_retries=3)                 
    return 
