import re,pytz,calendar,pdb,csv
from datetime import datetime, timedelta
import dateutil.parser as dparser
from appointmentscheduler.models  import AppschedulerBookings
from django.shortcuts import  render, render_to_response,HttpResponseRedirect,HttpResponse
from dicttoxml import dicttoxml
from io import BytesIO
from operator import itemgetter

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle

def exportbookings(request):
	error_message = ""
	if request.method == "POST":
		# pdb.set_trace()
		duration = request.POST['coming_period']
		docformat = request.POST['format']
		operation_type = request.POST['type']

		today = datetime.now()
		user_timezone = request.session['visitor_timezone']
		visitor_tz = pytz.timezone(user_timezone[0])
		date_string= today.strftime("%Y-%m-%d") 
		datetime_without_tz_today  =dparser.parse(date_string)
		datetime_with_tz_today = visitor_tz.localize(datetime_without_tz_today, is_dst=None)
		# print(datetime_with_tz_today)	
		bookingsdetails = list()
		if duration == "coming":
			bookings_done = AppschedulerBookings.objects.all()
			for bkdn in bookings_done:
				bookingtime_done = bkdn.date.astimezone(pytz.timezone(user_timezone[0]))
				if bookingtime_done > datetime_with_tz_today:
					bookingid = bkdn.id
					bookingdetails = getbookingdetails( bookingid, user_timezone ) 
					bookingsdetails.append( bookingdetails )
		else:
			dates_list = getdatelist(duration, visitor_tz, datetime_with_tz_today )
			year = dates_list[0].year
			bookings_done = AppschedulerBookings.objects.filter(date__year = year)
			for bkdn in bookings_done:
				bookingtime_done = bkdn.date.astimezone(pytz.timezone(user_timezone[0])).date()
				for dateselected in dates_list:
					if bookingtime_done.day == dateselected.day and bookingtime_done.month == dateselected.month:
			#create a booked list and prepare dictionary
						bookingid = bkdn.id
						bookingdetails = getbookingdetails( bookingid, user_timezone ) 
						bookingsdetails.append( bookingdetails )
		# create xml or pdf or csv as requested  
		
		#get the booking id and all other details and create dictionary
		if len(bookingsdetails):
			if docformat == "csv":
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename='+ "bookings" + duration + "." + docformat
				headings = bookingsdetails[0].keys()
				csvWriter = csv.DictWriter(response, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
				csvWriter.writeheader()
				for data in bookingsdetails:
					csvWriter.writerow(data)
			if docformat == "xml":
				xml = dicttoxml(bookingsdetails, custom_root='Bookings', attr_type=False)
				response = HttpResponse( xml,content_type='application/xml')
				response['Content-Disposition'] = 'attachment; filename='+ "bookings" + duration + "." + docformat

			if docformat == "pdf":
				fields =list()
				for key in bookingsdetails[0].keys():

					fields.append((key,key))
				buffer = BytesIO()

				doc = DataToPdf(fields, bookingsdetails, 
				                title='Log Files Over 1MB')
				doc.export(buffer)
				response = HttpResponse( content_type='application/xml')
				response['Content-Disposition'] = 'attachment; filename='+ "bookings" + duration + "." + docformat
				pdf = buffer.getvalue()
				buffer.close()
				response.write(pdf)
			return 	response
		else:
			error_message ="Booking not available for this " + duration
	template_name = "exportbookings.html"
	return render(request, template_name, {"error_message" : error_message })   


def getbookingdetails( bookingid , user_timezone):
	booking_instance = AppschedulerBookings.objects.filter(id = bookingid)[0]
	booked_details = dict()
	booked_details['id'] = booking_instance.id
	booked_details['booking_id'] = booking_instance.bookingid
	booked_details['booking_price'] = round(float(booking_instance.booking_price),2)
	booked_details['booking_total'] = round(float(booking_instance.booking_total),2)
	booked_details['booking_deposit'] = round(float(booking_instance.booking_deposit),2)
	booked_details['booking_tax'] = round(float(booking_instance.booking_tax),2)
	booked_details['booking_status'] = booking_instance.booking_status
	booked_details['c_name'] = booking_instance.c_name  if booking_instance.c_name else ''
	booked_details['c_email'] = booking_instance.c_email if booking_instance.c_email else ''
	booked_details['c_phone'] = str(booking_instance.c_phone) if booking_instance.c_phone else ''
	booked_details['country'] = booking_instance.country.CountryName  if booking_instance.country else ''
	booked_details['c_city'] = booking_instance.c_city  if booking_instance.c_city else ''
	booked_details['c_state'] = booking_instance.c_state if booking_instance.c_state else ''
	booked_details['c_zip'] = booking_instance.c_zip if booking_instance.c_zip else ''
	booked_details['c_address_1'] = booking_instance.c_address_1 if booking_instance.c_address_1 else ''
	booked_details['c_address_2'] = booking_instance.c_address_2 if booking_instance.c_address_2 else ''
	booked_details['c_notes'] = booking_instance.c_notes if booking_instance.c_notes else ''
	booked_details['ip'] = booking_instance.ip
	booked_details['emp_name'] = booking_instance.employee.emp_name
	booked_details['service_name'] = booking_instance.service.service_name
	booked_details['service_duration'] = booking_instance.service.total
	booked_details['booking_date'] = booking_instance.date.astimezone(pytz.timezone(user_timezone[0]))
	booked_details['service_start_time'] = booking_instance.service_start_time.astimezone(pytz.timezone(user_timezone[0]))
	booked_details['service_end_time'] = booking_instance.service_end_time.astimezone(pytz.timezone(user_timezone[0]))
	booked_details['subscribed_email'] = 'Yes' if booking_instance.subscribed_email else 'No'
	booked_details['subscribed_sms'] = 'Yes' if booking_instance.subscribed_sms else 'No'
	booked_details['reminder_email'] = 'Yes' if booking_instance.reminder_email else 'No'
	booked_details['reminder_sms'] = 'Yes' if booking_instance.reminder_sms else 'No'

	return booked_details

def getdatelist(duration, visitor_tz, datetime_with_tz_today ):
	dates_list = list()
	if duration == "today":
		dates_list.append( datetime_with_tz_today )

	#Yesterday
	elif duration == "tomorrow":
		yesterday=datetime_with_tz_today + timedelta(days=1)
		yesterday_string= yesterday.strftime("%Y-%m-%d") 
		datetime_without_tz_tomorrow  =dparser.parse(yesterday_string)
		datetime_with_tz_tomorrow = visitor_tz.localize(datetime_without_tz_tomorrow, is_dst=None)
		print(datetime_with_tz_tomorrow)
		dates_list.append( datetime_with_tz_tomorrow )


	#This week or last week
	elif duration in ["nextweek", "thisweek"]:

		weekday = datetime_with_tz_today.weekday()
		start_delta = timedelta(days=weekday)
		start_of_week = datetime_with_tz_today - start_delta
		if duration == "nextweek":
			start_of_week = start_of_week + timedelta(days=7)

		for day in range(7):
			dates_list.append(start_of_week + timedelta(days=day))

	#This Month:
	elif duration in ["thismonth", "nextmonth"]:
		first_day_month=datetime_with_tz_today.replace(day=1)
		last_day_month = first_day_month.replace(day=calendar.monthrange(datetime_with_tz_today.year,datetime_with_tz_today.month)[1])
	#Last Month
		if duration == "nextmonth":
			first_day_month  = last_day_month + timedelta(days=1)
			last_day_month =  first_day_month.replace(day=calendar.monthrange(first_day_month.year,first_day_month.month)[1])

		print(first_day_month)
		print(last_day_month)
		print(int((last_day_month - first_day_month).days)+1)

		print("==================================================================================")
		dates_list = [ first_day_month + timedelta(n) for n in range(int((last_day_month - first_day_month).days)+1)]
	return dates_list



class DataToPdf():
    """
    Export a list of dictionaries to a table in a PDF file.
    """

    def __init__(self, fields, data, sort_by=None, title=None):
        """
        Arguments:
            fields - A tuple of tuples ((fieldname/key, display_name))
                specifying the fieldname/key and corresponding display
                name for the table header.
            data - The data to insert to the table formatted as a list of
                dictionaries.
            sort_by - A tuple (sort_key, sort_order) specifying which field
                to sort by and the sort order ('ASC', 'DESC').
            title - The title to display at the beginning of the document.
        """
        self.fields = fields
        self.data = data
        self.title = title
        self.sort_by = sort_by

    def export(self, filename, data_align='LEFT', table_halign='LEFT'):
        """
        Export the data to a PDF file.

        Arguments:
            filename - The filename for the generated PDF file.
            data_align - The alignment of the data inside the table (eg.
                'LEFT', 'CENTER', 'RIGHT')
            table_halign - Horizontal alignment of the table on the page
                (eg. 'LEFT', 'CENTER', 'RIGHT')
        """
        doc = SimpleDocTemplate(filename, pagesize=letter)

        styles = getSampleStyleSheet()
        styleH = styles['Heading1']

        story = []

        if self.title:
            story.append(Paragraph(self.title, styleH))
            story.append(Spacer(1, 0.25 * inch))

        if self.sort_by:
            reverse_order = False
            if (str(self.sort_by[1]).upper() == 'DESC'):
                reverse_order = True

            self.data = sorted(self.data,
                               key=itemgetter(self.sort_by[0]),
                               reverse=reverse_order)

        converted_data = self.__convert_data()
        table = Table(converted_data, hAlign=table_halign)
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN',(0, 0),(0,-1), data_align),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))

        story.append(table)
        doc.build(story)

    def __convert_data(self):
        """
        Convert the list of dictionaries to a list of list to create
        the PDF table.
        """
        # Create 2 separate lists in the same order: one for the
        # list of keys and the other for the names to display in the
        # table header.
        keys, names = zip(*[[k, n] for k, n in self.fields])
        new_data = [names]

        for d in self.data:
            new_data.append([d[k] for k in keys])

        return new_data
