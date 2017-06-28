# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
import re,pdb

class AppschedulerBookings(models.Model):
    uuid = models.CharField(unique=True, max_length=12, blank=True, null=True)
    calendar_id = models.IntegerField(blank=True, null=True)
    booking_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    booking_total = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    booking_deposit = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    booking_tax = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    booking_status = models.CharField(max_length=9, blank=True, null=True)
    payment_method = models.CharField(max_length=10, blank=True, null=True)
    c_name = models.CharField(max_length=255, blank=True, null=True)
    c_email = models.CharField(max_length=255, blank=True, null=True)
    c_phone = models.CharField(max_length=255, blank=True, null=True)
    c_country_id = models.IntegerField(blank=True, null=True)
    c_city = models.CharField(max_length=255, blank=True, null=True)
    c_state = models.CharField(max_length=255, blank=True, null=True)
    c_zip = models.CharField(max_length=255, blank=True, null=True)
    c_address_1 = models.CharField(max_length=255, blank=True, null=True)
    c_address_2 = models.CharField(max_length=255, blank=True, null=True)
    c_notes = models.TextField(blank=True, null=True)
    cc_type = models.CharField(max_length=255, blank=True, null=True)
    cc_num = models.CharField(max_length=255, blank=True, null=True)
    cc_exp_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    cc_exp_month = models.CharField(max_length=2, blank=True, null=True)
    cc_code = models.CharField(max_length=255, blank=True, null=True)
    txn_id = models.CharField(max_length=255, blank=True, null=True)
    processed_on = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    locale_id = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_bookings'


class AppschedulerBookingsServices(models.Model):
    tmp_hash = models.CharField(max_length=32, blank=True, null=True)
    booking_id = models.IntegerField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)
    employee_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    start_ts = models.IntegerField(blank=True, null=True)
    total = models.SmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    reminder_email = models.IntegerField(blank=True, null=True)
    reminder_sms = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_bookings_services'


class AppschedulerCalendars(models.Model):
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_calendars'


class AppschedulerDates(models.Model):
    foreign_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    start_lunch = models.TimeField(blank=True, null=True)
    end_lunch = models.TimeField(blank=True, null=True)
    is_dayoff = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_dates'
        unique_together = (('foreign_id', 'type', 'date'),)


class AppschedulerEmployees(models.Model):
    emp_name = models.CharField(max_length=255, blank=False, null=False)
    emp_notes = models.TextField(blank=False, null=False)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_subscribed = models.IntegerField(blank=True, null=True)
    is_subscribed_sms = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'appscheduler_employees'


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
    imagepath = "%s/%s/%s" %( "service" , instance.service_name, filename)
    return re.sub('\s+','',imagepath)

class AppschedulerServices(models.Model):
    PRIORITY_CHOICES = ((True, 'active'),
                        (False, 'inactive'),)
    service_name = models.CharField(max_length=100, unique=True,blank=True, null=True)
    service_desc = models.CharField(max_length=100, blank=True, null=True)
    service_img = models.ImageField(upload_to = service_img_location, default = 'service/no-img.jpg')
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    length = models.SmallIntegerField( blank=False, null=False)
    before = models.SmallIntegerField( blank=False, null=False)
    after = models.SmallIntegerField( blank=False, null=False)
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


    total = property( get_total)





class AppschedulerUsers(models.Model):

    role_id = models.IntegerField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
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


# class DjangoMigrations(models.Model):
    # app = models.CharField(max_length=255)
    # name = models.CharField(max_length=255)
    # applied = models.DateTimeField()

    # class Meta:
        # # managed = False
        # db_table = 'django_migrations'
