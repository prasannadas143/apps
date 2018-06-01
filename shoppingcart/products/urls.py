from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from .views.Catagories import listcatagories, AddCatagorie,MoveCatagories,EditCatagory, DeleteCatagory, DeleteCatagories
from .views.Products import AddProduct, Products, ListProducts, ProductDetail, Product, DeleteProduct,DeleteProducts, GetProductDetails, SearchProduct
from .views.Stock import InStock, listimages, deletestock
from .views.Stocks import listStock, deletestocks
from .views.Photos import BasicUploadView, DeletePhoto
from .views.Digital import digital
from .views.Attributes import attributes, delAttributeName, delAttribute, getallProducts, GetProductAttributes
from .views.SimilarProducts import ListSimilarProducts, SimilarProducts
from django.views.generic import TemplateView

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
    url(r'^ShowProducts/', TemplateView.as_view(template_name='Products.html'),name="ShowProducts"),
    url(r'^DeleteProduct/(?P<id>\d+)/$', DeleteProduct, name="DeleteProduct"),
    url(r'^DeleteProducts/', DeleteProducts, name="DeleteProducts"),
    url(r'^GetProductDetails/', GetProductDetails, name="GetProductDetails"),
    url(r'^SearchProduct/', SearchProduct, name="SearchProduct"),
    url(r'^(?P<id>\d+)/ProductDetail/$', ProductDetail, name="ProductDetail"),
    url(r'^getallProducts/', getallProducts, name="getallProducts"),
    url(r'^GetProductAttributes/', GetProductAttributes, name="GetProductAttributes"),



    url(r'^(?P<id>\d+)/SimilarProducts/',SimilarProducts,name="SimilarProducts"),
    url(r'^ListSimilarProducts/', ListSimilarProducts, name="ListSimilarProducts"),
    url(r'^(?P<id>\d+)/Extras/', TemplateView.as_view(template_name='Extras.html'),
        name="Extras"),

    url(r'^Stocks/', TemplateView.as_view(template_name='Stocks.html'), name="Stocks"),
    url(r'^ListStocks/', listStock , name="ListStocks"),
    url(r'^deletestocks/', deletestocks, name="deletestocks"),
    url(r'^(?P<id>\d+)/deletestock/$', deletestock, name='deletestock'),


    url(r'(?P<id>\d+)/$', Product, name="Product"),
    url(r'(?P<id>\d+)/InStock/$', InStock, name="AddStock"),

    url(r'^(?P<id>\d+)/Digital/$', digital, name='digital'),
    url(r'^(?P<id>\d+)/Attributes/', attributes, name="Attributes"),
    url(r'^(?P<id>\d+)/delAttributeName/$', delAttributeName, name="delAttributeName"),
    url(r'^(?P<id>\d+)/delAttribute/$', delAttribute, name="delAttribute"),

    url(r'^(?P<id>\d+)/photos/$', BasicUploadView.as_view(), name='photos'),
    url(r'^(?P<id>\d+)/listimages/$', listimages, name='listimages'),
    url(r'^(?P<productid>\d+)/deletephoto/(?P<id>\d+)/$', DeletePhoto, name='DeletePhoto'),

]