from django.conf.urls import url
from shoppingcart.clients import views as clients

urlpatterns = [
	
	url(r'^addClient/$', clients.addClient, name="addClient"),
    url(r'ClientList/$', clients.ClientList, name="ClientList"),
    url(r'Clients/$', clients.Clients, name="Clients"),
    url(r'^editClient/(?P<id>\d+)/$', clients.editClient, name="editClient"),
    url(r'^deleteClient/(?P<id>\d+)/$', clients.deleteClient, name="deleteClient"),

]
