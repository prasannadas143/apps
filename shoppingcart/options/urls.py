from django.conf.urls import url,include
from django.contrib import admin


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^CountryTemplate/',  include('shoppingcart.options.countries.urls') ),
	url(r'^backup/',  include('shoppingcart.options.Backup.urls'), name="backup"),

]