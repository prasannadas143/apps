from django.shortcuts import  render, HttpResponseRedirect,HttpResponse,get_object_or_404
import datetime,json,uuid
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt,ensure_csrf_cookie
from appointmentscheduler.models  import AppschedulerServices, AppschedulerEmployees, AppschedulerDates,AppschedulerCountries,AppschedulerBookings
import pytz,pdb
from datetime import datetime, timedelta
import dateutil.parser as dparser
from copy import deepcopy
from appointmentscheduler.form.bookingform import BookingForm

from appointmentscheduler.views.Options.Booking import BookingFormOptions,Payments,Options
import logging

logger = logging.getLogger(__name__)

@requires_csrf_token
def show_bookings(request):
    """ Displayes all booking information """
    template_name = "bookings.html"
    bookingdata = dict()
    user_timezone = request.session['visitor_timezone']
    bookings = AppschedulerBookings.objects.select_related('service').values('id', 'c_name', 'c_email'\
        ,"c_phone", "booking_status", "booking_total", 'service__service_name', "service_start_time" ).order_by('-id')
    bookingslist = []
    for booking in  bookings.iterator():
        bookingdetails = dict()
        bookingdetails["bookingid"] = booking['id']
        bookingdetails["c_name"] = booking['c_name']
        bookingdetails["c_email"] = booking['c_email']
        bookingdetails["c_phone"] = str(booking['c_phone'])
        bookingdetails["booking_status"] = booking['booking_status']
        bookingdetails["total"] = float(booking['booking_total'])
        bookingdetails["service_name"] = booking['service__service_name']
        getvisitortime = booking['service_start_time'].astimezone(pytz.timezone(user_timezone[0]))
        format = '%Y-%m-%d %H:%M %p'
        bookingdetails["booking_time"] = getvisitortime.strftime(format)
        bookingslist.append( bookingdetails )
    return  HttpResponse(json.dumps({"data" :bookingslist }), content_type='application/json')   

@requires_csrf_token
def editbooking(request, id=None):
    """ Edit booking """
    user_timezone = request.session['visitor_timezone']
    bookings = get_object_or_404( AppschedulerBookings,  pk=int(id) ) 
    bookings_old = deepcopy(bookings)
    errors =""
    template_name = "editbooking.html"

    # customer_fields = {
    # "c_country": "no",
    # "c_state" : "no", 
    # "c_city" : "no",
    # "c_zip"  : "no",
    # "c_name"  : "required",
    # "c_email" : "required",
    # "c_phone" : "required",
    # "c_address_1" : "no",
    # "c_address_2" : "no"
    # }
    # emailres=ckEditor.GetTemplateDetailByTemplateID(2)
    # SMSRes=ckEditor.GetSMSTemplateDetailByTemplateID(2)
    # # res=res.replace("{name}","Anupam Singh").replace("{date}","9:30").replace("{Day}","Monday")
    # SMSRes1 = SMSRes.format(Name="Anupam Singh",bookingID="B11-453ffdf665656", date="9:30",Day="29-10-2017")
    # emailres1 = emailres.format(Name="Anupam Singh",bookingID="B11-453ffdf665656", date="9:30",Day="29-10-2017")
    # #SMS.SendSMSDyncamic("727-723-4147 ",res1)
    # #EmailNotification.SendMailFromBooking("anupamsinghjadoun@gmail.com","TEST Subject",emailres1)
    customer_fields= BookingFormOptions.GetBookingValidation()
    # locals.update(payments_options)
    booking_options = Options.getbookingOptions()
    STEP = booking_options["STEP"]
    STATUS_IF_PAID =  booking_options["STATUS_IF_PAID"]
    STATUS_IF_NOT_PAID =  booking_options["STATUS_IF_NOT_PAID"]
    ACCEPT_BOOKING_BEFORE_START =  booking_options["ACCEPT_BOOKING_BEFORE_START"]
    CANCEL_BOOKING_BEFORE_START =   booking_options["CANCEL_BOOKING_BEFORE_START"]
    ACCEPT_BOOKING_AHEAD =  int(booking_options["ACCEPT_BOOKING_AHEAD"])

    default_status_if_paid = STATUS_IF_PAID
    default_status_if_not_paid = STATUS_IF_NOT_PAID
    bookingdetails = dict()

    if request.method == 'POST':
        formparams= request.POST.dict()
        request.POST._mutable = True
        request.POST.clear()
        payments_options = Payments.getPaymentOptions()
        DISABLE_PAYMENTS = int( payments_options["DISABLE_PAYMENTS"] )
        DEPOSIT_TYPE = payments_options["DEPOSIT_TYPE"]
        DEPOSIT = int( payments_options["DEPOSIT"] )
        TAX = int( payments_options["TAX"] )

        request.POST["bookingid"] = bookings.bookingid
        # verify price from form is same  with DB
        serviceid = formparams["service_booked_id"]
        price_db =  round(float(get_object_or_404( AppschedulerServices,  pk=int(serviceid) ).price),2)
        booking_price = formparams["booking_price"]  
        request.POST['booking_price'] = booking_price
        if not ( round(float(booking_price),2) == round(float(bookings.booking_price),2) \
               or round(float(booking_price),2) == round(float(price_db),2) ):
            return HttpResponse(status=403)

        booking_tax = formparams["booking_tax"]  
        request.POST['booking_tax'] = booking_tax
        request.POST['booking_notes'] = formparams["booking_notes"] 
        tax_percentage = TAX
        tax = price_db * round(float(tax_percentage/100),2)

        if not ( round(float(booking_tax),2) == round(float(bookings.booking_tax),2) \
           or round(float(booking_tax),2) == round(float(tax),2) ):
                return HttpResponse(status=403)

        booking_total =  round(float( formparams["booking_total"] ) ,2)

        request.POST['booking_total'] = booking_total
        total = round(float(booking_price),2) + round(float(booking_tax),2)
        # booking_total = round(float( formparams["booking_total"] ) ,2)
        # if round(float(total),2) == round(float(booking_total),2):
        #     request.POST['booking_total'] = total
        # else :
        #     return HttpResponse(status=403)
        if not ( round(float(booking_total),2) == round(float(bookings.booking_total),2) \
           or round(float(booking_total),2) == round(float(total),2) ):
                return HttpResponse(status=403)
        formparams['booking_deposit']=0  if not  formparams['booking_deposit'] else formparams['booking_deposit']
        booking_deposit = round(float(formparams['booking_deposit']),2)
        request.POST['booking_deposit'] = booking_deposit
        expected_deposit_percentage = DEPOSIT
        expected_booking_deposit = round(booking_total * float(expected_deposit_percentage/100),2)
        if not booking_deposit  >= expected_booking_deposit:
            errors += "need minimum booking deposit"

        status = formparams['booking_status']
  

        if round(float(booking_deposit),2) >= round(float(booking_total),2) :
            request.POST["booking_status"] = default_status_if_paid
        else :
            request.POST["booking_status"] = default_status_if_not_paid

     
        user_timezone = request.session['visitor_timezone']
        servicedate = formparams['svcdate']
        request.POST['date'] = getust(servicedate,user_timezone)
        service_start_time =  servicedate + " " +  formparams['svc_start_time'] 
        request.POST['service_start_time'] = getust(service_start_time,user_timezone)


        service_end_time =  servicedate + " " +  formparams['svc_end_time']
        request.POST['service_end_time'] = getust(service_end_time,user_timezone)

        employee_id = formparams['employeeid']
        if customer_fields['c_country'] in ["yes", "required"]:
            if 'c_country' in formparams and formparams['c_country']:
                country_id = formparams['c_country']
                countryobj =  get_object_or_404( AppschedulerCountries,  pk=int(country_id) )
            else :
                errors += "country field is required"
        serviceobj =  get_object_or_404( AppschedulerServices,  pk=int(serviceid) )
        employeeobj =  get_object_or_404( AppschedulerEmployees,  pk=int(employee_id) )


        request.POST['subscribed_email'] = int(formparams['subscribed_email_value'])
        request.POST['subscribed_sms'] = int(formparams['subscribed_sms_value'])
        request.POST['reminder_email'] = int(formparams['reminder_email_value'])
        request.POST['reminder_sms'] = int(formparams['reminder_sms_value'])
        request.POST['ip'] =  request.session['visitor_ip'] 
        request.POST['created'] = getust(str(datetime.now()), user_timezone)
        svc_start_time = request.POST['service_start_time']
        svc_end_time = request.POST['service_end_time']
        visitor_tz = pytz.timezone(str(user_timezone[0]))

        request.POST['time_zone'] =  visitor_tz

        bookings_done = AppschedulerBookings.objects.filter(employee=employee_id).exclude(id=id)
        svc_datetime = servicedate.split('-')
        year = int(svc_datetime[0].lstrip('0') )
        month = int(svc_datetime[1].lstrip('0') )
        day = int( svc_datetime[2].lstrip('0') )

        if valid_bookingdate(user_timezone, servicedate):
            msg = "Booking needs to be greater than today"
            errors += msg

        if  valid_bookingtime(user_timezone, servicedate, ACCEPT_BOOKING_AHEAD) :
            msg = "Booking needs to be " + str(ACCEPT_BOOKING_AHEAD) + " days before"
            errors += msg

        if get_valid_starttime(user_timezone, servicedate, formparams['svc_start_time'],\
         ACCEPT_BOOKING_BEFORE_START):
            msg = "Booking needs to be " + str(ACCEPT_BOOKING_BEFORE_START) + " hours before"
            errors += msg
      
        if not formparams['book_exist']:
            for bkdn in bookings_done.iterator():
                bookingtime_done = bkdn.date.astimezone(pytz.timezone(user_timezone[0])).date()

                if bookingtime_done.day == day and bookingtime_done.month == month and bookingtime_done.year == year:
                    start_time_db = bkdn.service_start_time
                    end_time_db =  bkdn.service_end_time   
                    if (svc_start_time >= start_time_db   and svc_start_time <= end_time_db)  or \
                    (svc_end_time >= start_time_db   and svc_end_time <= end_time_db):
                        
                        errors+=" change booking time slotsb: booking already existed"
                        break   
        for field,value in customer_fields.items():

            if field in formparams and  formparams[field] is not None:
                if field != 'c_country':
                    request.POST[field] = formparams[field]
                if customer_fields[field]  == "required":
                    if not customer_fields[field]:
                        errors += field + " field required"
                
        form = BookingForm(request.POST or None, instance=bookings )
        if errors :
            bookingdetails['formerrors'] = deepcopy( form.errors )
            bookingdetails['customerrors'] = errors           
            form.errors["customerror"] = errors


        # if form.errors:
        #     return render(request, template_name, {"form" : form })

        if form.is_valid():

            bookingobj = form.save(commit=False)
            bookingobj.service = serviceobj
            bookingobj.employee = employeeobj
            if 'c_country' in  customer_fields and  customer_fields['c_country'] in ['yes','required']:
                bookingobj.country = countryobj
            message = "Booking data is saved" 
            bookingobj.save()
            pdb.set_trace()
            bookingobj.send_email_sms("edit")
          
            return HttpResponseRedirect('/appointmentschduler/bookings/')
               

    bookingdetails['bookingdetails'] = bookings_old 
    Countries = AppschedulerCountries.objects.filter(status = 1 ).order_by('-id')
    country_info = []
    for Country in Countries.iterator():
        data=dict()
        data['id'] = Country.id
        data['CountryName'] = Country.CountryName
        country_info.append(data)
    todaydate= datetime.now().strftime("%Y-%m-%d")
    bookingdetails["defaultdate"] = todaydate 
    bookingdetails["customer_fields"] = customer_fields
    bookingdetails["countries"] = country_info 
    bookingdetails['svc_start_time'] = bookings_old.service_start_time.astimezone(pytz.timezone(user_timezone[0])).strftime( "%I:%M %p" )
    bookingdetails['svc_date'] = bookings_old.date.astimezone(pytz.timezone(user_timezone[0])).strftime("%Y-%m-%d")
    bookingdetails['svc_end_time'] = bookings_old.service_end_time.astimezone(pytz.timezone(user_timezone[0])).strftime("%I:%M %p")
    return render(request, template_name, bookingdetails)

@requires_csrf_token
def deletebooking(request,id=None):
    """ Delete booking """

    bookingobj = get_object_or_404( AppschedulerBookings,  pk=int(id) )
    bookingobj.delete()
    return  HttpResponse(status=204)   

@requires_csrf_token
def deletebookings(request):
    """ Delete list of booking """

    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        bookingobj=get_object_or_404( AppschedulerBookings,  pk=int(id) )
        bookingobj.delete()

    return  HttpResponse(status=204)   

@requires_csrf_token
def cancelbooking(request, id):
    """ cancel booking """

    user_timezone = request.session['visitor_timezone']
    booking = get_object_or_404( AppschedulerBookings,  pk=int(id) )
    booking_options = Options.getbookingOptions()
    CANCEL_BOOKING_BEFORE_START =  int( booking_options["CANCEL_BOOKING_BEFORE_START"] )
    
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    booking_todaydate = visitor_tz.localize(datetime_without_tz, is_dst=None)
    CANCEL_BOOKING_BEFORE_START =36
    expected_cancelled_date = booking_todaydate + timedelta(hours=CANCEL_BOOKING_BEFORE_START) 
    start_time_visitorzn = booking.service_start_time.astimezone(pytz.timezone(user_timezone[0]))
    if  expected_cancelled_date > start_time_visitorzn :
        data = { "accept_booking_before_start": CANCEL_BOOKING_BEFORE_START,
             "valid_booking" : True,
             }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else :
        data = { 
         "valid_booking" : True,
         }
        booking.booking_status = "cancelled"
        booking.save()
        booking.send_email_sms("cancel")
        return HttpResponse(json.dumps(data), content_type='application/json')

@requires_csrf_token
def addbooking(request):
    """ Add  booking """

    template_name = "addbooking.html"
    bookingdetails = dict()
    errors =""
    # customer_fields = {
    #     "c_country": "no",
    #     "c_state" : "no",
    #     "c_city" : "no",
    #     "c_zip"  : "no",
    #     "c_name"  : "required",
    #     "c_email" : "required",
    #     "c_phone" : "required",
    #     "c_address_1" : "no",
    #     "c_address_2" : "no"
    # }
    customer_fields= BookingFormOptions.GetBookingValidation()
    payments_options = Payments.getPaymentOptions()
    DISABLE_PAYMENTS = int( payments_options["DISABLE_PAYMENTS"] )
    DEPOSIT_TYPE = payments_options["DEPOSIT_TYPE"]
    DEPOSIT = int( payments_options["DEPOSIT"] )
    TAX = int( payments_options["TAX"] )
    booking_options = Options.getbookingOptions()
    STEP = booking_options["STEP"]
    STATUS_IF_PAID =  booking_options["STATUS_IF_PAID"]
    STATUS_IF_NOT_PAID =  booking_options["STATUS_IF_NOT_PAID"]
    ACCEPT_BOOKING_BEFORE_START =  booking_options["ACCEPT_BOOKING_BEFORE_START"]
    CANCEL_BOOKING_BEFORE_START =   booking_options["CANCEL_BOOKING_BEFORE_START"]
    ACCEPT_BOOKING_AHEAD =  int( booking_options["ACCEPT_BOOKING_AHEAD"] )
    default_status_if_paid = "confirmed"
    default_status_if_not_paid = "pending"
    if request.method == 'POST':
        formparams= request.POST.dict()
        request.POST._mutable = True
        request.POST.clear()


        request.POST["bookingid"] = formparams['uuid']
        # verify price from form is same  with DB
        serviceid = formparams["service_booked_id"]
        price_db =  round(float(get_object_or_404( AppschedulerServices,  pk=int(serviceid) ).price),2)
        booking_price = formparams["booking_price"]   
        if round(float(booking_price),2)== round(float(price_db),2):
            request.POST['booking_price'] = price_db
        else :
            return HttpResponse(status=403)

        booking_tax = formparams["booking_tax"]  
        tax_percentage = TAX
        tax = price_db * round(float(tax_percentage/100),2)

        if round(float(tax),2) == round(float(booking_tax),2):
            request.POST['booking_tax'] = round(float(tax),2)
        else :
            return HttpResponse(status=403)
        total = round(float(price_db),2) + round(float(tax),2)
        booking_total = round(float( formparams["booking_total"] ) ,2)
        if round(float(total),2) == round(float(booking_total),2):
            request.POST['booking_total'] = total
        else :
            return HttpResponse(status=403)
        if not formparams['booking_deposit'] :
            formparams['booking_deposit'] = 0 
        booking_deposit = round(float(formparams['booking_deposit']),2)
        request.POST['booking_deposit'] = booking_deposit
        expected_deposit_percentage = DEPOSIT
        expected_booking_deposit = round(booking_total * float(expected_deposit_percentage/100),2)
        if not booking_deposit  >= expected_booking_deposit:
            errors += "need minimum booking deposit"

        status = formparams['booking_status']
     

        if round(float(booking_deposit),2) >= round(float(booking_total),2) :
            request.POST["booking_status"] = default_status_if_paid
        else :
            request.POST["booking_status"] = default_status_if_not_paid

        # if formparams["c_country"] is not None:
        #     request.POST["c_country"] = formparams["c_country"]
        # if customer_fields["c_country"]  == "required":
        #     if not request.POST["c_country"]:
        #         errors += "Country field required"
        user_timezone = request.session['visitor_timezone']

        servicedate = formparams['servicedate']
        request.POST['date'] = getust(servicedate,user_timezone)
        service_start_time =  servicedate + " " +  formparams['svc_start_time'] 
        request.POST['service_start_time'] = getust(service_start_time,user_timezone)
        svc_start_time = request.POST['service_start_time']

        service_end_time =  servicedate + " " +  formparams['svc_end_time']
        request.POST['service_end_time'] = getust(service_end_time,user_timezone)
        svc_end_time = request.POST['service_end_time'] 
        employee_id = formparams['employeeid']
        if customer_fields['c_country'] in ["yes", "required"]:
            if 'c_country' in formparams and formparams['c_country']:
                country_id = formparams['c_country']
                countryobj =  get_object_or_404( AppschedulerCountries,  pk=int(country_id) )
            else :
                errors += "country field is required"
        serviceobj =  get_object_or_404( AppschedulerServices,  pk=int(serviceid) )
        employeeobj =  get_object_or_404( AppschedulerEmployees,  pk=int(employee_id) )


        request.POST['subscribed_email'] = int(formparams['subscribed_email_value'])
        request.POST['subscribed_sms'] = int(formparams['subscribed_sms_value'])
        request.POST['reminder_email'] = int(formparams['reminder_email_value'])
        request.POST['reminder_sms'] = int(formparams['reminder_sms_value'])
        visitor_tz = pytz.timezone(str(user_timezone[0]))
        request.POST['time_zone'] = visitor_tz
        request.POST['ip'] =  request.session['visitor_ip'] 
        request.POST['created'] = getust(str(datetime.now()), user_timezone)
        bookings_done = AppschedulerBookings.objects.filter(employee=employee_id)
        svc_datetime = servicedate.split('-')
        year = int(svc_datetime[0].lstrip('0') )
        month = int(svc_datetime[1].lstrip('0') )
        day = int( svc_datetime[2].lstrip('0') )
        # Throws error if booked time is already allotted
        if valid_bookingdate(user_timezone, servicedate):
            msg = "Booking needs to be greater than today"
            errors += msg

        if  valid_bookingtime(user_timezone, servicedate, ACCEPT_BOOKING_AHEAD) :
            msg = "Booking needs to be " + str(ACCEPT_BOOKING_AHEAD) + " days before"
            errors += msg

        if get_valid_starttime(user_timezone, servicedate, formparams['svc_start_time'],\
         ACCEPT_BOOKING_BEFORE_START):
            msg = "Booking needs to be " + str(ACCEPT_BOOKING_BEFORE_START) + " hours before"
            errors += msg

        if not formparams['book_exist']:
            for bkdn in bookings_done.iterator():
                bookingtime_done = bkdn.date.astimezone(pytz.timezone(user_timezone[0])).date()

                if bookingtime_done.day == day and bookingtime_done.month == month and bookingtime_done.year == year:
                    start_time_db = bkdn.service_start_time
                    end_time_db =  bkdn.service_end_time   
                    if (svc_start_time >= start_time_db   and svc_start_time <= end_time_db)  or \
                    (svc_end_time >= start_time_db   and svc_end_time <= end_time_db):
                        
                        errors+=" change booking time slotsb: booking already existed"
                        break
        for field,value in customer_fields.items():

            if field in formparams and  formparams[field] is not None:
                if field != 'c_country':
                    request.POST[field] = formparams[field]
                if customer_fields[field]  == "required":
                    if not customer_fields[field]:
                        errors += field + " field required"
        form = BookingForm(request.POST or None )
        if errors :
            bookingdetails['formerrors'] = deepcopy( form.errors )
            bookingdetails['customerrors'] = errors           
            form.errors["customerror"] = errors
        if form.is_valid():

            bookingobj = form.save(commit=False)
            bookingobj.service = serviceobj
            bookingobj.employee = employeeobj
            if 'c_country' in  customer_fields and  customer_fields['c_country'] in ['yes','required']:
                bookingobj.country = countryobj
            message = "Booking data is saved" 
            bookingobj.save()
            # bookingobj.send_email_sms("")
            return HttpResponseRedirect('/appointmentschduler/bookings/')

    bookingid = "BI" + str(uuid.uuid1().node)
    todaydate= datetime.now().strftime("%Y-%m-%d")
    appobjs = AppschedulerBookings.objects.all()
    if  not ("bookingid" in request.POST and request.POST["bookingid"] ):

        if appobjs.exists():
            lastbookingid = AppschedulerBookings.objects.latest('bookingid').bookingid

            newid = int(lastbookingid[-8:]) + 1
            bookingid = lastbookingid[:-8] + str(newid)

        else :
            bookingid = "BI" + str(uuid.uuid1().node)
    else :
        bookingid = request.POST['bookingid']

    Countries = AppschedulerCountries.objects.filter(status = 1 ).order_by('-id')
    country_info = []
    for Country in Countries.iterator():
        data=dict()
        data['id'] = Country.id
        data['CountryName'] = Country.CountryName
        country_info.append(data)
    bookingdetails["bookingid"] = bookingid
    bookingdetails["defaultdate"] = todaydate 
    bookingdetails["customer_fields"] = customer_fields
    bookingdetails["countries"] = country_info    
    return render(request, template_name, bookingdetails)

@csrf_exempt
def is_booking_exist(request):
    print("check existing booking")
    user_timezone = request.session['visitor_timezone']
    servicedate = request.GET['servicedate']
    svc_datetime = servicedate.split('-')
    year = int(svc_datetime[0].lstrip('0') )
    month = int(svc_datetime[1].lstrip('0') )
    day = int( svc_datetime[2].lstrip('0') )
    service_start_time =  servicedate + " " +  request.GET['svc_start_time'] 
    svc_start_time = getust(service_start_time,user_timezone)
    errors=""
    service_end_time =  servicedate + " " +  request.GET['svc_end_time']
    svc_end_time = getust(service_end_time,user_timezone)
    employee_id = request.GET['employeeid']
    if 'editflag' in request.GET and request.GET['editflag']:
        id = request.GET['id']
        bookings_done = AppschedulerBookings.objects.filter(employee=employee_id).exclude(id=id)
    else :
        bookings_done = AppschedulerBookings.objects.filter(employee=employee_id)

    for bkdn in bookings_done:
            bookingtime_done = bkdn.date.astimezone(pytz.timezone(user_timezone[0])).date()

            if bookingtime_done.day == day and bookingtime_done.month == month and bookingtime_done.year == year:
                start_time_db = bkdn.service_start_time
                end_time_db =  bkdn.service_end_time   
                if (svc_start_time >= start_time_db   and svc_start_time < end_time_db)  or \
                (svc_end_time > start_time_db   and svc_end_time <= end_time_db):
                    
                    errors+=" change booking time slotsb: booking already existed"
                    break
    return HttpResponse(errors)
@ensure_csrf_cookie
def employee_in_booking(request):
    """ Displays the employees available for the booking of a sevice """

    serviceid = request.GET['serviceid']
    servicedate = request.GET['servicedate']
    user_timezone = request.session['visitor_timezone']
    # convert the book date to ust time
    svc_datetime = servicedate.split('-')
    year = int(svc_datetime[0].lstrip('0') )
    month = int(svc_datetime[1].lstrip('0') )
    day = int( svc_datetime[2].lstrip('0') )

    # Prepare  timestamps from start_time to end_time with 30 min gap
    #Get the working hours for the given date
    adates = AppschedulerDates.objects.filter(date__year=year, visitor_timezone=user_timezone[0])
    booktime=None
    for dt in adates:
        getvisitortime = dt.date.astimezone(pytz.timezone(user_timezone[0]))
        if getvisitortime.date().day == day and getvisitortime.date().month == month:
            booktime = dt
            break
    #Create dateobj  if the date is not available in DB
    if not booktime :
        usttime = getust(servicedate,user_timezone)
        start_time_p = "9:30 AM"
        end_time_p = "5:30 PM"
        start_launch_p = "10:30 AM"
        end_launch_p = "11:30 AM"
        # prepare default string  with default value
        start_time_string = servicedate + " " + start_time_p
        start_time = getust(start_time_string,user_timezone)
        end_time_string = servicedate + " " + end_time_p
        end_time = getust(end_time_string,user_timezone)
        start_launch_string = servicedate + " " + start_launch_p
        start_launch = getust(start_launch_string,user_timezone)
        end_launch_string = servicedate + " " + end_launch_p
        end_launch = getust(end_launch_string,user_timezone)
        adt =AppschedulerDates(date=usttime, start_time=start_time, end_time=end_time,
              start_launch=start_launch, end_launch=end_launch, is_dayoff=0, visitor_timezone=user_timezone[0]  )
        adt.save()
    else :
        if booktime.is_dayoff:
            return HttpResponse(json.dumps({"error_message" : "This date is off" }) )
        else :
            start_time = booktime.start_time
            end_time = booktime.end_time
            start_launch = booktime.start_launch
            end_launch = booktime.end_launch

    # prepare the timstamps with 30 min gap
    workinghours = []
    next_time = start_time
    while next_time <= end_time :
        # add times to working hours list
        intervaltime = dict()
        intervaltime['interval'] = next_time
        intervaltime.setdefault('status', "on")
        if next_time >= start_launch and next_time <= end_launch:
            intervaltime['status'] = "off"
        next_time = next_time + timedelta(minutes=30)
        intervaltime['interval'] = intervaltime['interval'].astimezone(pytz.timezone(user_timezone[0])).strftime("%I:%M %p")
        workinghours.append(intervaltime)

    #Get the service duration
    serviceobj = get_object_or_404( AppschedulerServices,  pk=int(serviceid) ) 
    svc_duration = serviceobj.total
    # for workinghour in workinghours:
    #     svc_start_time = workinghour['interval']
    #     svc_end_time = svc_start_time + timedelta(minutes=svc_duration)
    #     # filter the off time also "launch time " and "end time"  ( all employee )
    #     if svc_end_time <= end_time  and not ((svc_end_time > start_launch) and (svc_end_time < end_launch)):
    #         workinghour['status'] = "on"
    #     workinghour['interval'] = workinghour['interval'].astimezone(pytz.timezone(user_timezone[0])).strftime("%I:%M %p")
       

    #Get all employee related to service
    employeelist = []
    appscheduleobj = get_object_or_404( AppschedulerServices,  pk=int(serviceid) ) 
    emp_service = appscheduleobj.emp_service.all()  
   
    if not emp_service.count() :
        return HttpResponse(json.dumps({"error_message" : "No employee is assiaciated with service" }) )


    for employee in emp_service:    
        # Mark it as off times also if  there is existing booking for the employee on the given time.

        # for empl_in_service in emp_service:
        #     if empl_in_service.id == employee.id:
        #         employee_info['checked'] = True
        # Get the working hours for the mentioned employee for the given date

        employee_info = dict([("name", employee.emp_name), ("id", employee.id),("image", employee.avatar.url),("workinghours" , workinghours)])
        employeelist.append(employee_info)
        # Validate  the end_time and enable  the start_time
        times = [] 
        svc_duration = 60

        for hour in employee_info["workinghours"] :
            datestr=servicedate + " " + hour["interval"]
            hour["interval_ust"] = getust(datestr,user_timezone)


        bookedtimes = []
        empid = employee.id
        #Get all bookings for the employee 
        bookings = AppschedulerBookings.objects.filter(employee_id=empid).exclude(booking_status="cancelled")

        #iterate all bookings and filter all booking for the requested date and the given employee.
            
        for bktm in bookings.iterator():
            bookingtime_local = bktm.date.astimezone(pytz.timezone(user_timezone[0])).date()

            if bookingtime_local.day == day and bookingtime_local.month == month and bookingtime_local.year == year:
                service_start_time = bktm.service_start_time
                service_end_time =  bktm.service_end_time
                bookedtime = { "start_time" : service_start_time , "end_time" : service_end_time }
                bookedtimes.append( bookedtime )
                
     
        #Mark the already booked time as "off" from working hours.          
                
        for bkdtime in bookedtimes:
            bktime_start = bkdtime["start_time"]
            bktime_end = bkdtime["end_time"]
            for wh in workinghours:
                wh_ust = wh["interval_ust"]
              
                # Keep status as "off" if working hours comes in already booked time.
                if wh_ust >= bktime_start   and wh_ust <= bktime_end :
                    wh["status"] = "off"
                    
        times = deepcopy(employee_info["workinghours"])
        times_count = len(times) 
        i = 0 

        while i < times_count-1:
            svc_end_time = times[i]["interval_ust"] + timedelta(minutes=svc_duration)
            cnt1 = i + 1
            flag = 0
            for j in range(cnt1, times_count)  :
                if svc_end_time <= times[j]["interval_ust"] :
                    if times[j-1]["status"] == 'on':
                        times[i]["end_hour"] = times[j]["interval"]
                        break;
                    elif times[j]["status"] == 'off' :
                        cnt2 = i
                        for k in range(cnt2,j+1) :
                            times[k]["status"] = "off"
                        cnt3= j+1
                        for p in range(cnt3, times_count-1):
                            if times[p]['status'] ==    'on':
                                times[p-1]['status']= 'on'
                                i = p-1
                                flag = 1
                                break 
                
                    if flag:
                        break
                elif svc_end_time > end_time:
                    times[i]["status"] = "off"
                    break

            if not flag:
                i = i+1
            
        times[times_count-1]["status"] = "off"
        employee_info["workinghours"] = deepcopy(times) 

        for hour in employee_info["workinghours"] :
            del hour["interval_ust"]

        # if no booking slots are available , show the error
        is_bookings_slot_na = False
        for employee in emp_service.iterator():    
            for hour in employee_info["workinghours"] :
                if hour['status'] == "on":
                    is_bookings_slot_na = is_bookings_slot_na | True
                    break
            if  is_bookings_slot_na:
                break       
        if not  is_bookings_slot_na:
            return HttpResponse( json.dumps({"error_message" : "slots are not available" }) )
    return HttpResponse(json.dumps(employeelist), content_type='application/json')

def get_serviceprice(request):
    """ Get the total price for a service """

    serviceids = request.GET.getlist('serviceids[]')
    (deposit, tax, total_price, total) = (0,0,0,0)
    default_status_if_paid = "confirmed"
    default_status_if_not_paid = "pending"

    for serviceid in serviceids:
        appscheduleobj = get_object_or_404( AppschedulerServices,  pk=int(serviceid) ) 

        price = float(appscheduleobj.price)
        total_price += price 
        payments_options = Payments.getPaymentOptions()
        DISABLE_PAYMENTS = int( payments_options["DISABLE_PAYMENTS"] )
        DEPOSIT_TYPE = payments_options["DEPOSIT_TYPE"]
        DEPOSIT = int( payments_options["DEPOSIT"] )
        TAX = int( payments_options["TAX"] )
        tax_percentage = TAX
        deposit_percentage = DEPOSIT
        deposit += round( price * (deposit_percentage/100), 2)
        tax += round(price * (tax_percentage/100),2)
        total += price + tax
    
    return HttpResponse(json.dumps({"price" : str(price) , "total_price": total_price, "tax" : tax ,
     "deposit" : deposit,"total" : total, "default_status_if_paid": default_status_if_paid,
     "default_status_if_not_paid" : default_status_if_not_paid } ), content_type='application/json')
  

def getust( date_string,user_timezone):
    """ Get Ust time """

    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    datetime_in_utc  = datetime_with_tz.astimezone(pytz.utc)
    return datetime_in_utc

def check_x_days_before(request):
    """ Verify  if booking can be done before x days  as per the options set"""

    servicedate = request.GET['servicedate']
    # convert it to visitor timezone.
    # get the current date.
    # ensure it is less than x days back
    # use timedelta to verify it 
# convert it to visitor timezone.
    # get the current date.
    # ensure it is less than x days back
    # use timedelta to verify it 
    user_timezone = request.session['visitor_timezone']
    booking_options = Options.getbookingOptions()
    ACCEPT_BOOKING_AHEAD =  int(booking_options["ACCEPT_BOOKING_AHEAD"])
    valid_booking = valid_bookingtime(user_timezone, servicedate, ACCEPT_BOOKING_AHEAD)
    data = { "accept_booking_ahead": ACCEPT_BOOKING_AHEAD,
             "valid_booking" : valid_booking }
    return HttpResponse(json.dumps(data), content_type='application/json')



def valid_bookingtime(user_timezone, servicedate, accept_booking_ahead):


    date_string= servicedate 
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    booking_datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    print(booking_datetime_with_tz)
    # below line is for testing , will be commented out 
    accept_booking_ahead = 0
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    booking_servicedate = visitor_tz.localize(datetime_without_tz, is_dst=None)
    print(booking_servicedate)
    two_days_timezone = booking_servicedate + timedelta(days=accept_booking_ahead)

    if  booking_datetime_with_tz.date() < booking_servicedate.date()  :
        return True

    if two_days_timezone.date() <= booking_datetime_with_tz.date() :
        return False
    else :
        return True

def valid_bookingdate(user_timezone, servicedate):
    """ Verify  if booking date is equal or greater than current date """


    date_string= servicedate 
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    booking_datetime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    print(booking_datetime_with_tz)
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    booking_todaydate = visitor_tz.localize(datetime_without_tz, is_dst=None)
    print(booking_todaydate)

    if  booking_datetime_with_tz.date() < booking_todaydate.date()  :
        return True

  
def check_x_hours_before(request):
    """ Verify  if booking can be done before x hours as per the options set """

    start_time = request.GET['start_time']
    servicedate = request.GET['servicedate']
    user_timezone = request.session['visitor_timezone']
    booking_options = Options.getbookingOptions()
    ACCEPT_BOOKING_BEFORE_START =  booking_options["ACCEPT_BOOKING_BEFORE_START"]

    valid_start_time = get_valid_starttime(user_timezone,servicedate,start_time,ACCEPT_BOOKING_BEFORE_START)
    data = { "accept_booking_before_start": ACCEPT_BOOKING_BEFORE_START,
             "valid_booking" : valid_start_time,
             }
    return HttpResponse(json.dumps(data), content_type='application/json')
 

def get_valid_starttime(user_timezone,servicedate,start_time, accept_booking_before_start):
    date_string =  servicedate + " " +  start_time 
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(date_string)
    service_starttime_with_tz = visitor_tz.localize(datetime_without_tz, is_dst=None)
    print(service_starttime_with_tz)
    # below line is for testing , will be commented out 
    accept_booking_before_start = 0
    visitor_tz = pytz.timezone(str(user_timezone[0]))
    datetime_without_tz  =dparser.parse(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    booking_todaydate = visitor_tz.localize(datetime_without_tz, is_dst=None)
    print(booking_todaydate)
    booking_start = booking_todaydate + timedelta(hours=accept_booking_before_start)
    if  service_starttime_with_tz < booking_todaydate  :
        return True

    if booking_start <= service_starttime_with_tz :
        return False
    else :
        return True   
