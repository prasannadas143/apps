from django.conf.urls import url

from .views import service,employees
urlpatterns = [
    url(r'^showservices/$', service.show_services, name="showservices"),
    url(r'^addservice/$', service.add_service , name="addservice"),
    url(r'^editservice/(?P<id>\d+)/$', service.edit_service, name="edit_service"),
    url(r'^addemployee/$', employees.add_Employee, name="addemployee"),
	url(r'^deleteimage/(?P<id>\d+)/$', service.edit_service, name="delete_service_image"),
    url(r'^deleteservice/(?P<id>\d+)/$', service.delete_service, name="delete_service"),
    url(r'^employeelist/$', employees.employee_List, name="employeelist"),
    url(r'^editemployee/(?P<id>\d+)/$', employees.edit_Employee, name="editEmployee"),
    url(r'^getemployees/$', employees.get_Employees, name="getemployees"),
    url(r'^listemployeesname/$', employees.employee_List, name="listemployeesname"),
]