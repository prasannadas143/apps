from django.conf.urls import url
from django.views.generic import TemplateView
from ..clients import views as clients

urlpatterns = [
	
	url(r'^addClient/$', clients.addClient, name="addClient"),
    url(r'getclients/$', clients.getclients, name="getclients"),
    url(r'listClients/$', TemplateView.as_view(template_name='Clients.html'), name="clients"),
    url(r'^editClient/(?P<id>\d+)/$', clients.editClient, name="editClient"),
    url(r'^deleteClient/(?P<id>\d+)/$', clients.deleteClient, name="deleteClient"),
    url(r'^deleteClients/$', clients.deleteClients, name="deleteClients"),
    url(r'^listphones/$', clients.list_phones, name="listphones"),
    url(r'^listemails/$', clients.list_emails, name="listemails"),

]
