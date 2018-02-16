from django.conf.urls import url,include
from django.contrib import admin
from .views import SMSConfig,SendMail,EmailConfig,SendSMS, \
listsms, deletesms, deletemultiplesms


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^SmsConfig/$',  SMSConfig, name="SmsConfig" ),
	url(r'^EmailConfig/$',  EmailConfig, name="EmailConfig"),
    url(r'^SendMail/$', SendMail, name="SendMail"),
    url(r'^SendSMS/$', SendSMS, name="SendSMS"),
	url(r'^listsms/$', listsms, name="listsms"),
    url(r'^deletesms/(?P<id>\d+)/$', deletesms, name="deletesms"),
    url(r'^deletemultiplesms/$', deletemultiplesms, name="deletemultiplesms"),

]