from django.conf.urls import url,include
from django.contrib import admin
from .views import SmsConfig,SendMail,EmailConfig,SendSMS

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^SmsConfig/',  SmsConfig, name="SmsConfig" ),
	url(r'^EmailConfig/',  EmailConfig, name="EmailConfig"),
    url(r'^SendMail/$', SendMail, name="SendMail"),
    url(r'^SendSMS/$', SendSMS, name="SendSMS"),

]