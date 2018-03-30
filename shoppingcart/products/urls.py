from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from .views.Catagories import Catagories, AddCatagorie


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^AddCatagorie/', AddCatagorie, name="AddCatagorie"),
    url(r'^Catagories/',  Catagories, name="Catagories"),

]