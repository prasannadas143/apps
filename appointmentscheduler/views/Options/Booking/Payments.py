from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from appointmentscheduler.models import  *
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.core import serializers
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField

def update_value(field_id, tab_id, newstep):
   item = AppschedulerOptions.objects.get(tab_id=int(tab_id), id = int(field_id) ) 
   getsteps = item.value.split('::')
   # get the user you want. (connect for example) in the var "user"
   if len(getsteps) == 2 :
      item.value = "{0}::{1}".format(getsteps[0], newstep )
   else :
      item.value = newstep ;
   #item.save()

@csrf_exempt
def PaymentOptions(request):
   # pdb.set_trace()
   tab_id = 7;
   message=None
   Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   paymentdata = dict()
   if request.method == 'POST':
      pdb.set_trace();
      for field in request.POST.keys():
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
      paymentdata['message'] ="opion is saved"
   else :

      item = AppschedulerOptions.objects.filter(tab_id=7)

      pdb.set_trace();

      #o_allow_authorize
      o_disable_paymentsList = item[11].value.split('::')
      o_disable_payments = o_disable_paymentsList[0].split('|')
      o_disable_payments_selected = o_disable_paymentsList[-1]
      o_disable_payments_id = item[11].id

      #o_deposit_type
      o_deposit_typeList = item[10].value.split('::')
      o_deposit_type = o_deposit_typeList[0].split('|')
      o_deposit_type_selected = o_deposit_typeList[-1]
      o_deposit_type_id = item[10].id

      #o_deposit
      o_deposit = item[9].value
      o_deposit_id = item[9].id

      #o_tax
      o_tax = item[13].value
      o_tax_id = item[13].id

     
      items = { "o_disable_paymentsList" : o_disable_paymentsList, "o_disable_payments_selected": o_disable_payments_selected,
      "o_deposit_typeList":o_deposit_type, "o_deposit_type_selected":o_deposit_type_selected,
     "o_deposit":o_deposit,"o_tax":o_tax,"o_disable_payments_id":o_disable_payments_id,"o_deposit_type_id":o_deposit_type_id,
     "o_deposit_id":o_deposit_id,"o_tax_id":o_tax_id
      }
      paymentdata['items'] = items
      # Then, do a redirect for example
   return render(request,'Payments.html', paymentdata)



