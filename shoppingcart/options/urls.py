from django.conf.urls import url,include
from django.contrib import admin
from appointmentscheduler.views.Options.Invoice import Invoice
from .Options import Options,Payments,BookingFormOptions,terms


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^CountryTemplate/',  include('shoppingcart.options.countries.urls') ),
	url(r'^backup/',  include('shoppingcart.options.Backup.urls'), name="backup"),
    url(r'^Company/$', Invoice.Company, name="Company"),
    url(r'^SmsEmailSettings/', include('shoppingcart.options.SmsEmailSettings.urls'), name="SmsEmailSettings"),
	url(r'^BookingOptions/$', Options.BookingOptions, name="BookingOptions"),
	url(r'^PaymentOptions/$', Payments.PaymentOptions, name="PaymentOptions"),
	url(r'^BookingFormOptions/$', BookingFormOptions.BookingFormOptions, name="BookingFormOptions"), 
    url(r'^terms/$', terms.terms, name="terms"),

]