from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from .views.Catagories import listcatagories, AddCatagorie,MoveCatagories,EditCatagory, DeleteCatagory, DeleteCatagories
from .views.Products import AddProduct, Products, ListProducts, ProductDetail, Product
from .views.Photos import BasicUploadView, DeletePhoto
from .views.Digital import digital
from .views.Attributes import attributes, delAttributeName, delAttribute
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
    url(r'(?P<id>\d+)/$', Product, name="Product"),

    url(r'^(?P<id>\d+)/photos/$', BasicUploadView.as_view(), name='photos'),
    url(r'^(?P<id>\d+)/Digital/$', digital, name='digital'),
    url(r'^(?P<id>\d+)/ProductDetail/$', ProductDetail, name="ProductDetail"),
    url(r'^(?P<id>\d+)/Attributes/', attributes, name="Attributes"),
    url(r'^(?P<id>\d+)/delAttributeName/$', delAttributeName, name="delAttributeName"),
    url(r'^(?P<id>\d+)/delAttribute/$', delAttribute, name="delAttribute"),

    url(r'^(?P<productid>\d+)/deletephoto/(?P<id>\d+)/$', DeletePhoto, name='DeletePhoto'),

]