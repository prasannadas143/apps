from django.conf.urls import url,include
from django.contrib import admin
from appointmentscheduler.views.Options.Invoice import Invoice
from .Options import Options,Payments,CheckoutForm,terms


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^CountryTemplate/',  include('shoppingcart.options.countries.urls') ),
	url(r'^backup/',  include('shoppingcart.options.Backup.urls'), name="backup"),
    url(r'^Company/$', Invoice.Company, name="Company"),
    url(r'^SmsEmailSettings/', include('shoppingcart.options.SmsEmailSettings.urls'), name="SmsEmailSettings"),
    url(r'^SmsEmailTemplates/', include('shoppingcart.options.SmsEmailTemplates.urls'), name="SmsEmailTemplates"),
    url(r'^ShippingAndTax/', include('shoppingcart.options.ShippingAndTax.urls'), name="ShippingAndTax"),
    url(r'^BookingOptions/$', Options.BookingOptions, name="BookingOptions"),
	url(r'^PaymentOptions/$', Payments.PaymentOptions, name="PaymentOptions"),
	url(r'^CheckoutFormOptions/$', CheckoutForm.CheckoutFormOptions, name="CheckoutFormOptions"), 
    url(r'^terms/$', terms.terms, name="terms"),


]