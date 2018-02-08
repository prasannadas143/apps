from django.conf.urls import url
from django.views.generic import TemplateView
from shoppingcart.options.Backup import views as backup

urlpatterns = [	
	url(r'^showbackups/$', backup.create_backup, name="backup"),
    url(r'^listbackup/$', backup.listbackups, name="listbackups"),
    url(r'^deletebackup/(?P<id>\d+)/$', backup.deletebackup, name="deletebackup"),
    url(r'^deletebackups/$', backup.deletebackups, name="deletebackups"),
    url(r'^downloadbackup/(?P<id>\d+)/$', backup.downloadbackup, name="downloadbackup"),

]