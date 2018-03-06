from django.conf.urls import url,include
from django.contrib import admin
from .views import addshipping, deleteshipping

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^shipping/',  addshipping ),
    url(r'^deleteshipping/' , deleteshipping)

]    