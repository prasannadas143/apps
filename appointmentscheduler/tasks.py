from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task
from .celery import app as celery_app
from django.conf import settings

import arrow
import os,pdb
import smtplib
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

@shared_task
def send_sms(appointment_id):
    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        appointment = AppschedulerBookings.objects.get(pk=appointment_id)
    except AppschedulerBookings.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return
    SMSRes=ckEditor.GetSMSTemplateDetailByTemplateID(2)
    SMSRes1 = SMSRes.format(Name="Anupam Singh",bookingID="B11-453ffdf665656", date="9:30",Day="29-10-2017")
    SMS.SendSMSDyncamic("727-723-4147 ",SMSRes1)

   
@shared_task  
def send_email(booking):  
    bookingid = booking.pk
    templateid = 2
    tmpdtls=ckEditor.GetTemplateDetailByTemplateID(templateid)
    emailres = tmpdtls.DesignedTemplate
    Subject = tmpdtls.subject


    tab_id = 5;
    item = AppschedulerOptions.objects.filter(tab_id=tab_id)
    o_FromEmail = item[0].value;
    o_FromEmailPassword = item[1].value;
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