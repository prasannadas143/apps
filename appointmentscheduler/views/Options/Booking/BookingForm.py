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
from json import dump, load

def update_value(field_id, tab_id, newstep):
   item = AppschedulerOptions.objects.get(tab_id=int(tab_id), id = int(field_id))
   getsteps = item.value.split('::')
   # get the user you want. (connect for example) in the var "user"
   if len(getsteps) >1 :
      item.value = "{0}::{1}".format(getsteps[0], newstep )
   else :
      item.value = newstep ;
   item.save()

@csrf_exempt
def BookingFormOptions(request):
   tab_id = 4;
   message=None
   Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   BookingFormdata = dict()
   if request.method == 'POST':
      for field in request.POST.keys():
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
         BookingFormdata['message'] ="Booking opion is saved"

   item = AppschedulerOptions.objects.filter(tab_id=4)
   o_bf_zipList = item[11].value.split('::')
   o_bf_zip = o_bf_zipList[0].split('|')
   o_bf_zip_selected = o_bf_zipList[-1]
   o_bf_zip_id = item[11].id

   labels = item[11].label.split('::')[0].split('|')
   o_bf_termsList = item[10].value.split('::')
   o_bf_terms = o_bf_termsList[0].split('|')
   o_bf_terms_selected = o_bf_termsList[-1]
   o_bf_terms_id = item[10].id


   o_bf_stateList = item[9].value.split('::')
   o_bf_state = o_bf_stateList[0].split('|')
   o_bf_state_selected = o_bf_stateList[-1]
   o_bf_state_id = item[9].id

   o_bf_phoneList = item[8].value.split('::')
   o_bf_phone = o_bf_phoneList[0].split('|')
   o_bf_phone_selected = o_bf_phoneList[-1]
   o_bf_phone_id = item[8].id

   o_bf_notesList = item[8].value.split('::')
   o_bf_notes = o_bf_phoneList[0].split('|')
   o_bf_notes_selected = o_bf_phoneList[-1]
   o_bf_notes_id = item[8].id
  

   o_bf_nameList = item[7].value.split('::')
   o_bf_name = o_bf_nameList[0].split('|')
   o_bf_name_selected = o_bf_nameList[-1]
   o_bf_name_id = item[7].id


   o_bf_emailList = item[6].value.split('::')
   o_bf_email = o_bf_emailList[0].split('|')
   o_bf_email_selected = o_bf_emailList[-1]
   o_bf_email_id = item[6].id

   o_bf_countryList = item[5].value.split('::')
   o_bf_country = o_bf_emailList[0].split('|')
   o_bf_country_selected = o_bf_emailList[-1]
   o_bf_country_id = item[5].id
   

   o_bf_cityList = item[4].value.split('::')
   o_bf_city = o_bf_cityList[0].split('|')
   o_bf_city_selected = o_bf_cityList[-1]
   o_bf_city_id = item[4].id


   o_bf_captchaList = item[3].value.split('::')
   o_bf_captcha = o_bf_captchaList[0].split('|')
   o_bf_captcha_selected = o_bf_captchaList[-1]
   o_bf_captcha_id = item[3].id

   o_bf_address_2List = item[2].value.split('::')
   o_bf_address_2 = o_bf_cityList[0].split('|')
   o_bf_address_2_selected = o_bf_cityList[-1]
   o_bf_address_2_id = item[2].id

   o_bf_address_1List = item[1].value.split('::')
   o_bf_address_1 = o_bf_address_1List[0].split('|')
   o_bf_address_1_selected = o_bf_address_1List[-1]
   o_bf_address_1_id = item[1].id

 
   showlabels= {'1': "No", '2': "Yes", '3' : "Yes(required)"}
   
   items = {"o_bf_zipList":o_bf_zip,"o_bf_zip_selected":o_bf_zip_selected,"o_bf_zip_id":o_bf_zip_id,
   "o_bf_terms":o_bf_terms,"o_bf_terms_selected":o_bf_terms_selected,"o_bf_terms_id":o_bf_terms_id,
   "o_bf_state":o_bf_state,"o_bf_state_selected":o_bf_state_selected,"o_bf_state_id":o_bf_state_id,
   "o_bf_phone":o_bf_phone,"o_bf_phone_selected":o_bf_phone_selected,"o_bf_phone_id":o_bf_phone_id,
   "o_bf_notes":o_bf_notes,"o_bf_notes_selected":o_bf_notes_selected,"o_bf_notes_id":o_bf_notes_id,
   "o_bf_name" : o_bf_name,"o_bf_name_selected":o_bf_name_selected,"o_bf_name_id":o_bf_name_id,
   "o_bf_email":o_bf_email,"o_bf_email_selected":o_bf_email_selected,"o_bf_email_id":o_bf_email_id,
   "o_bf_country":o_bf_country,"o_bf_country_selected":o_bf_country_selected,"o_bf_country_id":o_bf_country_id,
   "o_bf_city":o_bf_city,"o_bf_city_selected":o_bf_city_selected,"o_bf_city_id":o_bf_city_id,
   "o_bf_captcha":o_bf_captcha,"o_bf_captcha_selected":o_bf_captcha_selected,"o_bf_captcha_id":o_bf_captcha_id,
   "o_bf_address_2":o_bf_address_2,"o_bf_address_2_selected":o_bf_address_2_selected,"o_bf_address_2_id":o_bf_address_2_id,
   "o_bf_address_1":o_bf_address_1,"o_bf_address_1_selected":o_bf_address_1_selected,"o_bf_address_1_id":o_bf_address_1_id,
   "showlabels": showlabels}

   BookingFormdata['items'] = items
   return render(request,'BookingForm.html', BookingFormdata)