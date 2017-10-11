from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task
from .celery import app as celery_app
from django.conf import settings

import arrow
import os,pdb
import smtplib
from twilio.rest import Client

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from appointmentscheduler.models import AppschedulerBookings
from appointmentscheduler.views.Options.SMS import SMS
from appointmentscheduler.views.Options.Editor import ckEditor
from appointmentscheduler.views.Options.Booking import EmailNotification
from appointmentscheduler.views.Options.Editor import ckEditor
from appointmentscheduler.models import AppschedulerBookings, AppschedulerOptions
# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables

@task(bind=True, default_retry_delay=2*60)  
def send_sms(self,bookingid,opertype):
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
            smstmpdtls =" customername {customer_name} bookingid {bookingid} date {date} day {day}"
       
        customer_name = booking.c_name
        bookingid = booking.bookingid
        date = booking.service_start_time.astimezone(booking.time_zone).strftime( "%I:%M %p" )
        day = booking.date.astimezone(booking.time_zone).strftime("%Y-%m-%d")
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
      
        tab_id = 101;
        item = AppschedulerOptions.objects.filter(tab_id=tab_id)
        TWILIO_ACCOUNT_SID = item[0].value;
        print(TWILIO_ACCOUNT_SID);
        TWILIO_AUTH_TOKEN = item[1].value;
        print(TWILIO_AUTH_TOKEN);
        TWILIO_FROM_NUMBER = item[2].value;
        print(TWILIO_FROM_NUMBER);
        client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
        result= client.api.account.messages.create(to=toNumber, from_=TWILIO_FROM_NUMBER,body=Message)
        print(result)


    except Exception as exc:
       # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=2*60)                 

    return 

@task(bind=True, default_retry_delay=2*60)  
def send_email(self,bookingid, opertype):
    try:
        booking = AppschedulerBookings.objects.get(pk=bookingid)
        templateid = 2
        opertype = opertype + "EMAIL"
        tmpdtls=ckEditor.GetTemplateDetailByTemplateID(opertype)
        if tmpdtls :
            emailres = tmpdtls.DesignedTemplate
            Subject = tmpdtls.subject
        else :
            emailres =" customername {customer_name} bookingid {bookingid} date {date} day {day}"



        tab_id = 5
        item = AppschedulerOptions.objects.filter(tab_id=tab_id)
        o_FromEmail = item[0].value
        o_FromEmailPassword = item[1].value
        customer_name = booking.c_name
        bookingid = booking.bookingid
        date = booking.service_start_time.astimezone(booking.time_zone).strftime( "%I:%M %p" )
        day = booking.date.astimezone(booking.time_zone).strftime("%Y-%m-%d")
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
        fromaddr = o_FromEmail
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

    except Exception as exc:
       # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=2*60)                 
    return 
