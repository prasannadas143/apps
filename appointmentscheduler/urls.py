from django.conf.urls import url

from .views import service,employees
from .views.Options import General
from .views.Options.Booking import Options,Payments,BookingForm
from .views.Options.WorkingTime import Default
from .views.Options.Countries import Countries

urlpatterns = [
    url(r'^showservices/$', service.show_services, name="showservices"),
    url(r'^listservices/$', service.list_services, name="listservices"),
    url(r'addservice/$', service.add_service , name="addservice"),
    url(r'^editservice/(?P<id>\d+)/$', service.edit_service, name="edit_service"),
    url(r'^addemployee/$', employees.add_Employee, name="addemployee"),
	url(r'^deleteimage/(?P<id>\d+)/$', service.deleteimage, name="delete_service_image"),
    url(r'^deleteemployeeimage/(?P<id>\d+)/$', employees.deleteemployeeimage, name="deleteemployeeimage"),
    url(r'^deleteservice/(?P<id>\d+)/$', service.delete_service, name="delete_service"),
    url(r'^deleteservices/$', service.delete_services, name="delete_services"),
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
    url(r'^updateGeneral/$', General.updateGeneral, name="updateGeneral"),
    url(r'^BookingOptions/$', Options.BookingOptions, name="BookingOptions"),
    url(r'associated_employee_names/(?P<id>\d+)/$', service.associated_employee_names, name="assiosiated_employees"),
    url(r'^PaymentOptions/$', Payments.PaymentOptions, name="PaymentOptions"),
    url(r'^BookingFormOptions/$', BookingForm.BookingFormOptions, name="BookingFormOptions"), 
    url(r'^WorkingTimeOptions/$', Default.WorkingTimeOptions, name="WorkingTimeOptions"),
    url(r'^addCountry/$', Countries.addCountry, name="addCountry"),
    url(r'^CountryList/$', Countries.CountriesList, name="CountryList"),
    url(r'^CountryTemplate/$', Countries.CountryTemplate, name="CountryTemplate"),
    url(r'^editCountry/(?P<id>\d+)/$', Countries.editCountry, name="editCountry"),
    url(r'^deleteCountry/(?P<id>\d+)/$', Countries.deleteCountry, name="deleteCountry"),
    url(r'associated_service_names/(?P<id>\d+)/$', employees.associated_service_names, name="assiosiated_services"),
]