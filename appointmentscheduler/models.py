# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.conf import settings
from .celery import app as celery_app

import re,pdb,os,datetime,uuid,arrow
from phonenumber_field.modelfields import PhoneNumberField
from django.core import validators
from timezone_field import TimeZoneField
from django.core.exceptions import ValidationError



class AppschedulerBookings(models.Model):
    bookingid = models.CharField(unique=True, max_length=18, blank=True, null=True)
    booking_price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    booking_total = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    booking_deposit = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    booking_tax = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    booking_status = models.CharField(max_length=9, blank=False, null=False)
    c_name = models.CharField(max_length=255, blank=True, null=True)
    c_email = models.EmailField( blank=False, null=False, validators=[validators.validate_email,])
    c_phone = PhoneNumberField(  blank=False, null=False)
    country = models.ForeignKey(
        'AppschedulerCountries',
        on_delete=models.CASCADE,
        related_name="country", blank=True,null=True
        
        
    ) 
    c_city = models.CharField(max_length=255, blank=True, null=True)
    c_state = models.CharField(max_length=255, blank=True, null=True)
    c_zip = models.CharField(max_length=255, blank=True, null=True)
    c_address_1 = models.TextField(blank=True, null=True)
    c_address_2 = models.TextField(blank=True, null=True)
    c_notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=False, null=False)
    ip = models.GenericIPAddressField( blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    service_start_time = models.DateTimeField(blank=False, null=False)
    service_end_time = models.DateTimeField(blank=False, null=False)
    subscribed_email = models.BooleanField(default=False)
    subscribed_sms = models.BooleanField(default=False)
    reminder_email = models.BooleanField(default=False)
    reminder_sms = models.BooleanField(default=False)
    time_zone = TimeZoneField(default='US/Pacific')

    # Additional fields not visible to users
    task_id_sms = models.CharField(max_length=50, blank=True, editable=False)
    task_id_email = models.CharField(max_length=50, blank=True, editable=False)

    
    employee = models.ForeignKey(
        'AppschedulerEmployees',
        on_delete=models.CASCADE,
        related_name="employee", blank=True,null=True
        
    ) 
    service = models.ForeignKey(
        'AppschedulerServices',
        on_delete=models.CASCADE,
        related_name="service", blank=True,null=True
        
    ) 
    
    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)
        
    def get_absolute_url(self):
        return "/editbooking/%i/" % self.id

    def get_duedate(self):
        return self.date

    def clean(self):
        """Checks that appointments are not scheduled in the past"""

        appointment_time = arrow.get(self.service_start_time, self.time_zone.zone)

        # if appointment_time < arrow.utcnow():
        #     raise ValidationError('You cannot schedule an appointment for the past. Please check your time and time_zone')



    def schedule(self, opertype):
        """Schedules a Celery task to send a reminder about this appointment"""

        # Calculate the correct time to send this reminder
        # appointment_time = arrow.get(self.service_start_time, self.time_zone.zone)
        appointment_time = arrow.get(self.service_start_time)

        reminder_time = appointment_time.replace(minutes=-settings.REMINDER_TIME)
        pdb.set_trace()
        # Schedule the Celery task
        from .tasks import send_email,send_sms
        if self.subscribed_email:
            send_email.apply_async((self.id,opertype,))
        if self.reminder_email:
            self.task_id_email = send_email.apply_async((self.id,opertype,), eta=reminder_time)
        if self.subscribed_sms:
            send_sms.apply_async((self.id,opertype,))
        if self.reminder_sms:
            self.task_id_sms = send_sms.apply_async((self.id,opertype,), eta=reminder_time)
        # send_sms(self.id,opertype, reminder_time)
        # send_email(self.id,opertype, reminder_time)

        return 

    def send_email_sms(self, opertype):
        """Custom save method which also schedules a reminder"""
        # Check if we have scheduled a reminder for this appointment before
        if self.task_id_sms:
            # Revoke that task in case its time has changed
            celery_app.control.revoke(self.task_id_sms)
        if self.task_id_email:
            # Revoke that task in case its time has changed
            celery_app.control.revoke(self.task_id_email)
        # Save our appointment, which populates self.pk,
        # which is used in schedule_reminder
        # Schedule a new reminder task for this appointment1
        self.schedule(opertype)
        
        # Save our appointment again, with the new task_id
  

    duedate = property( get_duedate )  
   

    class Meta:
        # managed = False
        db_table = 'appscheduler_bookings'




class AppschedulerCalendars(models.Model):
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_calendars'


class AppschedulerDates(models.Model):
    date = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_launch = models.DateTimeField(blank=True, null=True)
    end_launch = models.DateTimeField(blank=True, null=True)
    is_dayoff = models.BooleanField(default=False )
    visitor_timezone =  models.CharField(max_length=32,default='Europe/Istanbul',blank=False)
    class Meta:
        # managed = False
        db_table = 'appscheduler_dates'


def employee_img_location(instance, filename):
    filename, ext = os.path.splitext(filename.lower())
    filename = "%s_%s.%s" % (slugify(filename),datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S"), ext)
    imagepath = "%s/%s_%s/%s" %( "employee" ,instance.emp_name,instance.phone, filename)
    print(imagepath)
    return re.sub('[!@#$+\s]','',imagepath)


class AppschedulerEmployees(models.Model):
    emp_name = models.CharField(max_length=100, blank=False, null=False)
    emp_notes = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True,  validators=[validators.validate_email,])
    password = models.CharField(max_length=50)
    phone =  PhoneNumberField(unique=True,  blank=False, null=False)
    avatar = models.ImageField(upload_to=employee_img_location, default = 'employee/no-img.jpg')
    is_subscribed = models.BooleanField(default=False)
    is_subscribed_sms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
   

    class Meta:
        # managed = False
        db_table = 'appscheduler_employees'

    def service_count_in_employee(self):
        return self.appschedulerservices_set.count() 

    service_count = property( service_count_in_employee )

class AppschedulerInvoice(models.Model):
    booking = models.ForeignKey(
        'AppschedulerBookings',
        on_delete=models.CASCADE,
        related_name="invoice", blank=True,null=True
    
    )    
    invoiceid =  models.CharField(max_length=100)

    class Meta:
        # managed = False
        db_table = 'appscheduler_invoices'
  

class AppschedulerEmployeesServices(models.Model):
    employee_id = models.IntegerField()
    service_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'appscheduler_employees_services'
        unique_together = (('employee_id', 'service_id'),)


class AppschedulerFields(models.Model):
    key = models.CharField(unique=True, max_length=100, blank=True, null=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=6, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_fields'


class AppschedulerMultiLang(models.Model):
    foreign_id = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    locale = models.IntegerField(blank=True, null=True)
    field = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_multi_lang'
        unique_together = (('foreign_id', 'model', 'locale', 'field'),)


class AppschedulerOptions(models.Model):
    foreign_id = models.IntegerField()
    key = models.CharField(max_length=255)
    tab_id = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=6)
    order = models.IntegerField(blank=True, null=True)
    is_visible = models.IntegerField(blank=True, null=True)
    style = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_options'


class AppschedulerRoles(models.Model):
    role = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=1)

    class Meta:
        # managed = False
        db_table = 'appscheduler_roles'


def service_img_location(instance, filename):
    # imagepath = "%s/%s/%s" %( "service" , instance.service_name, filename)
    filename, ext = os.path.splitext(filename.lower())
    filename = "%s_%s.%s" % (slugify(filename),datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S"), ext)
    imagepath = '%s/%s/%s' % ('service', instance.service_name,filename)
    return re.sub('[!@#$+\s]','',imagepath)

class AppschedulerServices(models.Model):
    PRIORITY_CHOICES = ((True, 'active'),
                        (False, 'inactive'),)
    service_name = models.CharField(max_length=100, unique=True, blank=False, null=False )
    service_desc = models.CharField(max_length=100, blank=True, null=True)
    service_img = models.ImageField(upload_to = service_img_location, default = 'service/no-img.jpg')
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    length = models.SmallIntegerField( blank=False, null=False, default= 0)
    before = models.SmallIntegerField( blank=False, null=False,default= 0)
    after = models.SmallIntegerField( blank=False, null=False,default= 0)
    total = models.SmallIntegerField()
    is_active = models.BooleanField(choices=PRIORITY_CHOICES,  default=True)
    emp_service = models.ManyToManyField(AppschedulerEmployees,  blank=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_services'
    #
    def get_total(self):
        setattr(self,"_total" , int(self.length + self.after + self.before))
        return self._total

    def employee_count_in_service(self):
        return self.emp_service.count() 

    total = property( get_total )
    emp_count = property( employee_count_in_service )





class AppschedulerUsers(models.Model):

    role_id = models.IntegerField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    status = models.CharField(max_length=1)
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_users'


class AppschedulerWorkingTimes(models.Model):
    foreign_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    monday_from = models.TimeField(blank=True, null=True)
    monday_to = models.TimeField(blank=True, null=True)
    monday_lunch_from = models.TimeField(blank=True, null=True)
    monday_lunch_to = models.TimeField(blank=True, null=True)
    monday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    tuesday_from = models.TimeField(blank=True, null=True)
    tuesday_to = models.TimeField(blank=True, null=True)
    tuesday_lunch_from = models.TimeField(blank=True, null=True)
    tuesday_lunch_to = models.TimeField(blank=True, null=True)
    tuesday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    wednesday_from = models.TimeField(blank=True, null=True)
    wednesday_to = models.TimeField(blank=True, null=True)
    wednesday_lunch_from = models.TimeField(blank=True, null=True)
    wednesday_lunch_to = models.TimeField(blank=True, null=True)
    wednesday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    thursday_from = models.TimeField(blank=True, null=True)
    thursday_to = models.TimeField(blank=True, null=True)
    thursday_lunch_from = models.TimeField(blank=True, null=True)
    thursday_lunch_to = models.TimeField(blank=True, null=True)
    thursday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    friday_from = models.TimeField(blank=True, null=True)
    friday_to = models.TimeField(blank=True, null=True)
    friday_lunch_from = models.TimeField(blank=True, null=True)
    friday_lunch_to = models.TimeField(blank=True, null=True)
    friday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    saturday_from = models.TimeField(blank=True, null=True)
    saturday_to = models.TimeField(blank=True, null=True)
    saturday_lunch_from = models.TimeField(blank=True, null=True)
    saturday_lunch_to = models.TimeField(blank=True, null=True)
    saturday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    sunday_from = models.TimeField(blank=True, null=True)
    sunday_to = models.TimeField(blank=True, null=True)
    sunday_lunch_from = models.TimeField(blank=True, null=True)
    sunday_lunch_to = models.TimeField(blank=True, null=True)
    sunday_dayoff = models.CharField(max_length=1, blank=True, null=True)
    class Meta:
        # managed = False
        db_table = 'appscheduler_working_times'
        unique_together = (('foreign_id', 'type'),)

class AppschedulerCountries(models.Model):
    CountryName = models.CharField(max_length=200, blank=False, null=False,unique=True)
    Alpha2 = models.CharField(max_length=6,blank=True, null=True)
    Alpha3 = models.CharField(max_length=6, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_countries'
        unique_together = (('CountryName'),)

# class DjangoMigrations(models.Model):
    # app = models.CharField(max_length=255)
    # name = models.CharField(max_length=255)
    # applied = models.DateTimeField()

    # class Meta:
        # # managed = False
        # db_table = 'django_migrations'


class AppschedulerTemplates(models.Model):
    TemplateName = models.CharField(max_length=200, blank=False, null=False,unique=True)
    status = models.BooleanField(default=True)
    class Meta:
        # managed = False
        db_table = 'appscheduler_templates'
        unique_together = (('TemplateName'),)

class AppschedulerTemplatesDetails(models.Model):
    TemplateID = models.CharField(max_length=200, blank=False, null=False,unique=True)
    subject = models.CharField(max_length=200, blank=False, null=False)
    DesignedTemplate = models.TextField(blank=False, null=False)
    status = models.BooleanField(default=True)
    class Meta:
        # managed = False
        db_table = 'appscheduler_TemplatesDetails'
        unique_together = (('TemplateID'),)  

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
