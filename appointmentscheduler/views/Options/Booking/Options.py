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
   if len(getsteps[0].split('|')) == 2  and getsteps[0].split('|')[1] == 0 :
      getsteps[0] = "{0}::{1}".format(newstep, getsteps.split('|')[1] )
   steps = "{0}::{1}".format(getsteps[0], newstep)
   item.value = steps
   item.save()

@csrf_exempt
def BookingOptions(request):
   # pdb.set_trace()
   tab_id = 3;
   message=None
   Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   if request.method == 'POST':
      pdb.set_trace();
      for field in request.POST.keys():
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
      message="opion is saved"
   else :

      item = AppschedulerOptions.objects.filter(tab_id=3)
      getsteps = item[4].value.split('::')
      steps = getsteps[0].split('|')
      step_selected = getsteps[-1]
      step_id = item[4].id

      status_if_paid = item[3].value.split('::')
      status_if_paid_list = status_if_paid[0].split('|')
      status_if_paid_selected = status_if_paid[-1]
      status_id= item[3].id
      
      status_if_not_paid = item[2].value.split('::')
      status_if_not_paid_list = status_if_not_paid[0].split('|')
      status_if_not_paid_selected = status_if_not_paid[-1]
      status_not_id= item[2].id


      hide_prices = item[1].value.split("::")
      hide_prices_list=hide_prices[0].split('|')
      hide_prices_list_selected=hide_prices[-1]
      hide_prices_id = item[1].id


      accept_booking_ahead = item[5].value.split("::")
      accept_booking_ahead_list=accept_booking_ahead[0].split('|')
      accept_booking_ahead_selected=accept_booking_ahead[-1]
      accept_booking_ahead_id = item[5].id


      accept_booking = item[0].value.split("::")
      accept_booking_list=accept_booking[0].split('|')
      accept_booking_selected=accept_booking[-1]
      accept_booking_id = item[0].id


      items = { "steps" : steps, "step_selected": step_selected,"status_if_paid_list":status_if_paid_list,
      "status_if_paid_selected":status_if_paid_selected,"status_if_not_paid_list":status_if_not_paid_list,
      "status_if_not_paid_selected":status_if_not_paid_selected,"hide_prices_list":hide_prices_list,
      "hide_prices_list_selected":hide_prices_list_selected,"accept_booking_list":accept_booking_list,
      "accept_booking_selected":accept_booking_selected, "step_id":  step_id, "status_id": status_id, "status_not_id": status_not_id,
      "accept_booking_ahead_selected" : accept_booking_ahead_selected,
      "hide_prices_id": hide_prices_id, "accept_booking_id" : accept_booking_id, "accept_booking_ahead_id" : accept_booking_ahead_id


      }
      # Then, do a redirect for example
   return render(request,'Options.html', {'items':items ,"message":message })



