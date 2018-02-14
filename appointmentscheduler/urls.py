from django.conf.urls import url
from .views import bookings,dashboard
from .views.exportbookings import BookingsFeed

from .views import service,employees,invoice,exportbookings,report
from .views.Options import General
from .views.Options.Booking import Options,Payments,BookingFormOptions,EmailNotification,terms
from .views.Options.WorkingTime import Default, DefaultTime
from .views.Options.Countries import Countries
from .views.Options.Invoice import Invoice
from .views.Options.Editor import ckEditor
from .views.Options.Backup import backup
from django.views.generic import TemplateView
from .views.Options.SMS import SMS


urlpatterns = [

   url(r'^services/$', service.show_services, name="showservices"),
    url(r'^listservices/$', service.list_services, name="listservices"),
    url(r'addservice/$', service.add_service , name="addservice"),
    url(r'^editservice/(?P<id>\d+)/$', service.edit_service, name="edit_service"),
    url(r'^deleteservice/(?P<id>\d+)/$', service.delete_service, name="delete_service"),
    url(r'^deleteservices/$', service.delete_services, name="delete_services"),
    url(r'^listServicesName/$', employees.services_names, name="listServicesName"),
    url(r'^deleteimage/(?P<id>\d+)/$', service.deleteimage, name="delete_service_image"),
    url(r'associated_employee_names/(?P<id>\d+)/$', service.associated_employee_names, name="assiosiated_employees"),

 
    url(r'^addemployee/$', employees.add_Employee, name="addemployee"),
    url(r'^deleteemployeeimage/(?P<id>\d+)/$', employees.deleteemployeeimage, name="deleteemployeeimage"),
    url(r'^employeelist/$', employees.employee_List, name="employeelist"),
    url(r'^getemployees/$', employees.getemployees, name="getemployees"),
    url(r'^editemployee/(?P<id>\d+)/$', employees.edit_Employee, name="editEmployee"),
    url(r'^delete_employee/(?P<id>\d+)/$', employees.delete_employee, name="deleteemployee"),
    url(r'^delete_employees/$', employees.delete_employees, name="deleteemployees"),
    url(r'^getemployees/$', employees.get_Employees, name="getemployees"),
    url(r'^listemployeesname/$', service.employee_names, name="listemployeesname"),
    url(r'^listServicesName/$', employees.services_names, name="listServicesName"),
    url(r'^listphones/$', employees.list_phones, name="listphones"),
    url(r'^listemails/$', employees.list_emails, name="listemails"),
    url(r'^deleteEmployee/(?P<id>\d+)/$', employees.delete_employee, name="deleteEmployee"),
    url(r'associated_service_names/(?P<id>\d+)/$', employees.associated_service_names, name="assiosiated_services"),

    # url(r'^updateGeneral/$', General.updateGeneral, name="updateGeneral"),
    url(r'^BookingOptions/$', Options.BookingOptions, name="BookingOptions"),
    url(r'^PaymentOptions/$', Payments.PaymentOptions, name="PaymentOptions"),
    url(r'^BookingFormOptions/$', BookingFormOptions.BookingFormOptions, name="BookingFormOptions"), 

    url(r'^CustomTimeOptions/$', DefaultTime.CustomtimeOptions, name="customtimeoptions"),
    url(r'^Customtimes/$', DefaultTime.ShowCustomtimes, name="customtimes"),
    url(r'^delcustomtime/(?P<id>\d+)/$', DefaultTime.DeleteCustomtime, name="delcustomtime"),
    url(r'^delcustomtimes/$', DefaultTime.DeleteCustomtimes, name="delcustomtimes"),
    url(r'^editcustomtime/(?P<id>\d+)/$', DefaultTime.CustomtimeOptions, name="editcustomtimes"),

    url(r'^WorkingTimeOptions/$', Default.WorkingTimeOptions, name="WorkingTimeOptions"),
    url(r'^WorkingTimeOptionsEdit/$', Default.WorkingTimeOptionsEdit, name="WorkingTimeOptionsEdit"),
    url(r'^addCountry/$', Countries.addCountry, name="addCountry"),
    url(r'^CountryList/$', Countries.CountriesList, name="CountryList"),
    url(r'^CountryTemplate/$', Countries.CountryTemplate, name="CountryTemplate"),
    url(r'^editCountry/(?P<id>\d+)/$', Countries.editCountry, name="editCountry"),
    url(r'^deleteCountry/(?P<id>\d+)/$', Countries.deleteCountry, name="deleteCountry"),
    url(r'^Company/$', Invoice.Company, name="Company"),

    url(r'^getbookings/$', bookings.show_bookings, name="bookings"),
    url(r'^bookings/$', TemplateView.as_view(template_name='bookings.html'), name="bookings"),
    url(r'^editbooking/(?P<id>\d+)/$', bookings.editbooking, name="editbooking"),
    url(r'^deletebooking/(?P<id>\d+)/$', bookings.deletebooking, name="deletebooking"),
    url(r'^deletebookings/$', bookings.deletebookings, name="delete_bookings"),
    url(r'^is_booking_exist/$', bookings.is_booking_exist, name="is_booking_exist"),
    url(r'^addbooking/$', bookings.addbooking, name="addbooking"),
    url(r'^employee_in_booking/$', bookings.employee_in_booking, name="employeeinbooking"),
    url(r'^getserviceprice/$', bookings.get_serviceprice, name ="getserviceprice"),
    url(r'^cancelbooking/(?P<id>\d+)/$', bookings.cancelbooking, name ="cancelbooking"),
    url(r'^check_x_days_before/$', bookings.check_x_days_before, name ="check_x_days_before"),
    url(r'^check_x_hours_before/$', bookings.check_x_hours_before, name ="check_x_hours_before"),



    url(r'^getinvoices/$', invoice.list_invoices, name ="getinvoice"),
    url(r'^getinvoice/(?P<id>\d+)/$', invoice.generate_invoice, name ="getinvoice"),
    url(r'^printinvoice/(?P<id>\d+)/$', invoice.print_invoice_pdf, name ="getinvoicepdf"),
    url(r'^invoices/$', TemplateView.as_view(template_name='invoices.html'), name="bookings"),
    url(r'^delete_invoices/$', invoice.delete_invoices, name ="delete_invoices"),
    url(r'^delete_invoice/(?P<id>\d+)/$', invoice.delete_invoice, name ="delete_invoice"),
    url(r'^sendmail_invoice/$', invoice.sendmail_invoice, name ="sendmail_invoice"),
    url(r'^sendmsg_invoice/$', invoice.sendmsg_invoice, name ="sendmsg_invoice"),


    url(r'^dashboard/$', dashboard.dashboard, name="dashboard"),
    url(r'^getdashboarddetails/$', dashboard.getdashboarddetails, name="getdashboarddetails"),
    url(r'^printdashboard/$', dashboard.printdashboard),
    url(r'^exportbookings/$', exportbookings.exportbookings, name="exportbookings"),

    url(r'^employee_report/$', report.employee_report, name="employee_report"),
    url(r'^employee_report_details/$', report.employee_report_details, name="employee_report_details"),
    url(r'^service_report/$', report.service_report, name="service_report"),
    url(r'^service_report_details/$', report.service_report_details, name="service_report_details"),


    url(r'^EditorTemplate/$', ckEditor.EditorTemplate, name="EditorTemplate"),
    url(r'^SaveTemplate/$', ckEditor.SaveTemplate, name="SaveTemplate"),
    url(r'^Template/$', ckEditor.Template, name="Template"),
    url(r'^AddTemplate/$', ckEditor.AddTemplate, name="AddTemplate"),
    url(r'^CheckDuplicateTemplate/$', ckEditor.CheckDuplicateTemplate, name="CheckDuplicateTemplate"),
    url(r'^Templates/$', ckEditor.Templates, name="Templates"),
    url(r'^TemplateList/$', ckEditor.TemplateList, name="TemplateList"),
    url(r'^deleteTemplate/$', ckEditor.deleteTemplate, name="deleteTemplate"),
    url(r'^EditorTemplatemplate/(?P<id>\d+)/$', ckEditor.editTemplate, name="editTemplate"),
    url(r'^GetTemplateDetails/$', ckEditor.GetTemplateDetails, name="GetTemplateDetails"),
    url(r'^TemplateDetailsList/$', ckEditor.TemplateDetailsList, name="TemplateDetailsList"),
    url(r'^TemplateDetailsData/$', ckEditor.TemplateDetailsData, name="TemplateDetailsData"),
    url(r'^UpdateTemplate/(?P<id>\d+)/$', ckEditor.UpdateTemplate, name="UpdateTemplate"),

    url(r'^SMSConfig/$', SMS.SMSConfig, name="SMSConfig"),
    url(r'^SendSMS/$', SMS.SendSMS, name="SendSMS"),
    url(r'^SendMail/$', EmailNotification.SendMail, name="SendMail"),
    url(r'^SaveMailSettings/$', EmailNotification.SaveMailSettings, name="SaveMailSettings"),
    url(r'^listsms/$', SMS.listsms, name="listsms"),
    url(r'^deletesms/(?P<id>\d+)/$', SMS.deletesms, name="deletesms"),
    url(r'^deletemultiplesms/$', SMS.deletemultiplesms, name="deletemultiplesms"),

    url(r'^backup/$', backup.create_backup, name="backup"),
    url(r'^listbackups/$', backup.listbackups, name="listbackups"),
    url(r'^deletebackup/(?P<id>\d+)/$', backup.deletebackup, name="deletebackup"),
    url(r'^deletebackups/$', backup.deletebackups, name="deletebackups"),
    url(r'^downloadbackup/(?P<id>\d+)/$', backup.downloadbackup, name="downloadbackup"),

    url(r'^terms/$', terms.terms, name="terms"),


    url(r'^latest/', BookingsFeed()),



]


# urlpatterns += patterns('',
#     # ...
#     (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
#         {'feed_dict': feeds}),
#     # ...
# )