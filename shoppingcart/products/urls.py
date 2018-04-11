from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from .views.Catagories import listcatagories, AddCatagorie,MoveCatagories,EditCatagory, DeleteCatagory, DeleteCatagories
from .views.Products import AddProduct, Products, ListProducts

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^AddCatagorie/', AddCatagorie, name="AddCatagorie"),
    url(r'^EditCatagory/(?P<id>\d+)/$', EditCatagory, name="EditCatagory"),
    url(r'^Catagories/',  listcatagories, name="Catagories"),
    url(r'^uparrow/(?P<id>\d+)/$', MoveCatagories, name="uparrow"),
    url(r'^downarrow/(?P<id>\d+)/$', MoveCatagories, name="downarrow"),
    url(r'^DeleteCatagory/$', DeleteCatagory, name="deletecatagory"),
    url(r'^DeleteCatagories/$', DeleteCatagories, name="DeleteCatagories"),

    url(r'^AddProduct/', AddProduct, name="AddProduct"),
    url(r'^ListProducts/', ListProducts, name="ListProducts"),

]