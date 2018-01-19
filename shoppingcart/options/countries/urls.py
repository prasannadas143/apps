from django.conf.urls import url
from shoppingcart.options.countries import views as Countries

urlpatterns = [
	
	url(r'^addCountry/$', Countries.addCountry, name="addCountry"),
    url(r'CountryList/$', Countries.CountriesList, name="CountryList"),
    url(r'Countries/$', Countries.CountryTemplate, name="CountryTemplate"),
    url(r'^editCountry/(?P<id>\d+)/$', Countries.editCountry, name="editCountry"),
    url(r'^deleteCountry/(?P<id>\d+)/$', Countries.deleteCountry, name="deleteCountry"),

]
