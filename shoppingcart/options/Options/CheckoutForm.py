from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token
from shoppingcart.options.models import  Options
import pdb


tab_id = 102;
app_name = "shoppingcart"
def update_value(field_id, tab_id, newstep):
   item =   get_object_or_404( Options,  tab_id=int(tab_id),\
    id = int(field_id) )
   getsteps = item.value.split('::')
   # get the user you want. (connect for example) in the var "user"
   if len(getsteps) >1 :
      item.value = "{0}::{1}".format(getsteps[0], newstep )
   else :
      item.value = newstep ;
   item.save()

@requires_csrf_token
def CheckoutFormOptions(request):
   message=None
   # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   CheckoutFormdata = dict()

   if request.method == 'POST':
      for field in request.POST.keys():
         if field == 'csrfmiddlewaretoken':
            continue
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
      messages.success(request, 'CheckoutForm options are updated.')

   items = Options.objects.filter(tab_id=tab_id,app_name=app_name\
      ).values('id','key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item

   sc_sb_name_dict = items_dict['sc_sb_name']
   sc_sb_nameList = sc_sb_name_dict['value'].split('::')
   sc_sb_name_all = sc_sb_nameList[0].split('|')
   sc_sb_name_selected = sc_sb_nameList[-1]
   sc_sb_name_id = sc_sb_name_dict['id']

   sc_sb_country_dict = items_dict['sc_sb_country']
   sc_sb_countryList = sc_sb_country_dict['value'].split('::')
   sc_sb_country_all = sc_sb_countryList[0].split('|')
   sc_sb_country_selected = sc_sb_countryList[-1]
   sc_sb_country_id = sc_sb_country_dict['id']

   sc_sb_city_dict = items_dict['sc_sb_city']
   sc_sb_cityList = sc_sb_city_dict['value'].split('::')
   sc_sb_city_all = sc_sb_cityList[0].split('|')
   sc_sb_city_selected = sc_sb_cityList[-1]
   sc_sb_city_id = sc_sb_city_dict['id']

   sc_sb_state_dict = items_dict['sc_sb_state']
   sc_sb_stateList = sc_sb_state_dict['value'].split('::')
   sc_sb_state_all = sc_sb_stateList[0].split('|')
   sc_sb_state_selected = sc_sb_stateList[-1]
   sc_sb_state_id = sc_sb_state_dict['id']

   sc_sb_zip_dict = items_dict['sc_sb_zip']
   sc_sb_zipList = sc_sb_zip_dict['value'].split('::')
   sc_sb_zip_all = sc_sb_zipList[0].split('|')
   sc_sb_zip_selected = sc_sb_zipList[-1]
   sc_sb_zip_id = sc_sb_zip_dict['id']

   sc_sb_address_1_dict = items_dict['sc_sb_address_1']
   sc_sb_address_1List = sc_sb_address_1_dict['value'].split('::')
   sc_sb_address_1_all = sc_sb_address_1List[0].split('|')
   sc_sb_address_1_selected = sc_sb_address_1List[-1]
   sc_sb_address_1_id = sc_sb_address_1_dict['id']

   sc_sb_address_2_dict = items_dict['sc_sb_address_2']
   sc_sb_address_2List = sc_sb_address_2_dict['value'].split('::')
   sc_sb_address_2_all = sc_sb_address_2List[0].split('|')
   sc_sb_address_2_selected = sc_sb_address_2List[-1]
   sc_sb_address_2_id = sc_sb_address_2_dict['id']

   sc_sd_name_dict = items_dict['sc_sd_name']
   sc_sd_nameList = sc_sd_name_dict['value'].split('::')
   sc_sd_name_all = sc_sd_nameList[0].split('|')
   sc_sd_name_selected = sc_sd_nameList[-1]
   sc_sd_name_id = sc_sd_name_dict['id']

   
   sc_sd_country_dict = items_dict['sc_sd_country']
   sc_sd_countryList = sc_sd_country_dict['value'].split('::')
   sc_sd_country_all = sc_sd_countryList[0].split('|')
   sc_sd_country_selected = sc_sd_countryList[-1]
   sc_sd_country_id = sc_sd_country_dict['id']
 
   sc_sd_city_dict = items_dict['sc_sd_city']
   sc_sd_cityList = sc_sd_city_dict['value'].split('::')
   sc_sd_city_all = sc_sd_cityList[0].split('|')
   sc_sd_city_selected = sc_sd_cityList[-1]
   sc_sd_city_id = sc_sd_city_dict['id']

   sc_sd_state_dict = items_dict['sc_sd_city']
   sc_sd_stateList = sc_sd_state_dict['value'].split('::')
   sc_sd_state_all = sc_sd_stateList[0].split('|')
   sc_sd_state_selected = sc_sd_stateList[-1]
   sc_sd_state_id = sc_sd_state_dict['id']

   sc_sd_zip_dict = items_dict['sc_sd_zip']
   sc_sd_zipList = sc_sd_zip_dict['value'].split('::')
   sc_sd_zip_all = sc_sd_zipList[0].split('|')
   sc_sd_zip_selected = sc_sd_zipList[-1]
   sc_sd_zip_id = sc_sd_zip_dict['id']


   sc_sd_address_1_dict = items_dict['sc_sd_address_1']
   sc_sd_address_1List = sc_sd_address_1_dict['value'].split('::')
   sc_sd_address_1_all = sc_sd_address_1List[0].split('|')
   sc_sd_address_1_selected = sc_sd_address_1List[-1]
   sc_sd_address_1_id = sc_sd_address_1_dict['id'] 
 
   sc_sd_address_2_dict = items_dict['sc_sd_address_2']
   sc_sd_address_2List = sc_sd_address_2_dict['value'].split('::')
   sc_sd_address_2_all = sc_sd_address_2List[0].split('|')
   sc_sd_address_2_selected = sc_sd_address_2List[-1]
   sc_sd_address_2_id = sc_sd_address_2_dict['id']

   sc_cl_name_dict = items_dict['sc_cl_name']
   sc_cl_nameList = sc_cl_name_dict['value'].split('::')
   sc_cl_name_all = sc_cl_nameList[0].split('|')
   sc_cl_name_selected = sc_cl_nameList[-1]
   sc_cl_name_id = sc_cl_name_dict['id']

   sc_cl_phone_dict = items_dict['sc_cl_phone']
   sc_cl_phoneList = sc_cl_phone_dict['value'].split('::')
   sc_cl_phone_all = sc_cl_phoneList[0].split('|')
   sc_cl_phone_selected = sc_cl_phoneList[-1]
   sc_cl_phone_id = sc_cl_phone_dict['id']

   sc_cl_website_dict = items_dict['sc_cl_website']
   sc_cl_websiteList = sc_cl_website_dict['value'].split('::')
   sc_cl_website_all = sc_cl_websiteList[0].split('|')
   sc_cl_website_selected = sc_cl_websiteList[-1]
   sc_cl_website_id = sc_cl_website_dict['id']


   sc_cl_notes_dict = items_dict['sc_cl_notes']
   sc_cl_notesList = sc_cl_notes_dict['value'].split('::')
   sc_cl_notes_all = sc_cl_notesList[0].split('|')
   sc_cl_notes_selected = sc_cl_notesList[-1]
   sc_cl_notes_id = sc_cl_notes_dict['id']

   sc_cl_captcha_dict = items_dict['sc_cl_captcha']
   sc_cl_captchaList = sc_cl_captcha_dict['value'].split('::')
   sc_cl_captcha_all = sc_cl_captchaList[0].split('|')
   sc_cl_captcha_selected = sc_cl_captchaList[-1]
   sc_cl_captcha_id = sc_cl_captcha_dict['id']

   sc_cl_terms_dict = items_dict['sc_cl_terms']
   sc_cl_termsList = sc_cl_terms_dict['value'].split('::')
   sc_cl_terms_all = sc_cl_termsList[0].split('|')
   sc_cl_terms_selected = sc_cl_termsList[-1]
   sc_cl_terms_id = sc_cl_terms_dict['id']
   showlabels= {'1': "No", '2': "Yes", '3' : "Yes(required)"}
   
   items ={
   "sc_sb_nameList":sc_sb_name_all,"sc_sb_name_selected":sc_sb_name_selected ,"sc_sb_name_id":sc_sb_name_id,
   "sc_sb_countryList":sc_sb_country_all,"sc_sb_country_selected":sc_sb_country_selected ,"sc_sb_country_id":sc_sb_country_id,
   "sc_sb_cityList":sc_sb_city_all,"sc_sb_city_selected":sc_sb_city_selected ,"sc_sb_city_id":sc_sb_city_id,
   "sc_sb_stateList":sc_sb_state_all,"sc_sb_state_selected":sc_sb_state_selected ,"sc_sb_state_id":sc_sb_state_id,
   "sc_sb_zipList":sc_sb_zip_all,"sc_sb_zip_selected":sc_sb_zip_selected ,"sc_sb_zip_id":sc_sb_zip_id,
   "sc_sb_address_1List":sc_sb_address_1_all,"sc_sb_address_1_selected":sc_sb_address_1_selected ,"sc_sb_address_1_id":sc_sb_address_1_id,
   "sc_sb_address_2List":sc_sb_address_2_all,"sc_sb_address_2_selected":sc_sb_address_2_selected ,"sc_sb_address_2_id":sc_sb_address_2_id,
   "sc_sd_nameList":sc_sd_name_all,"sc_sd_name_selected":sc_sd_name_selected ,"sc_sd_name_id":sc_sd_name_id,
   "sc_sd_countryList":sc_sd_country_all,"sc_sd_country_selected":sc_sd_country_selected ,"sc_sd_country_id":sc_sd_country_id,
   "sc_sd_cityList":sc_sd_city_all,"sc_sd_city_selected":sc_sd_city_selected ,"sc_sd_city_id":sc_sd_city_id,
   "sc_sd_stateList":sc_sd_state_all,"sc_sd_state_selected":sc_sd_state_selected ,"sc_sd_state_id":sc_sd_state_id,
   "sc_sd_zipList":sc_sd_zip_all,"sc_sd_zip_selected":sc_sd_zip_selected ,"sc_sd_zip_id":sc_sd_zip_id,
   "sc_sd_address_1List":sc_sd_address_1_all,"sc_sd_address_1_selected":sc_sd_address_1_selected ,"sc_sd_address_1_id":sc_sd_address_1_id,
   "sc_sd_address_2List":sc_sd_address_2_all,"sc_sd_address_2_selected":sc_sd_address_2_selected ,"sc_sd_address_2_id":sc_sd_address_2_id,
   "sc_cl_nameList":sc_cl_name_all,"sc_cl_name_selected":sc_cl_name_selected ,"sc_cl_name_id":sc_cl_name_id,
   "sc_cl_phoneList":sc_cl_phone_all,"sc_cl_phone_selected":sc_cl_phone_selected ,"sc_cl_phone_id":sc_cl_phone_id,
   "sc_cl_websiteList":sc_cl_website_all,"sc_cl_website_selected":sc_cl_website_selected ,"sc_cl_website_id":sc_cl_website_id,
   "sc_cl_notesList":sc_cl_notes_all,"sc_cl_notes_selected":sc_cl_notes_selected ,"sc_cl_notes_id":sc_cl_notes_id,
   "sc_cl_captchaList":sc_cl_captcha_all,"sc_cl_captcha_selected":sc_cl_captcha_selected ,"sc_cl_captcha_id":sc_cl_captcha_id,
   "sc_cl_termsList":sc_cl_terms_all,"sc_cl_terms_selected":sc_cl_terms_selected ,"sc_cl_terms_id":sc_cl_terms_id,
   "showlabels": showlabels
   }
   CheckoutFormdata['items'] = items
   templatename=  'CheckoutForm.html'

   return render(request,templatename, CheckoutFormdata)



def GetCheckoutFormOptions():
  
   items = Options.objects.filter(tab_id=tab_id).values('key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item

   sc_sb_name_dict = items_dict['sc_sb_name']
   sc_sb_nameList = sc_sb_name_dict['value'].split('::')
   sc_sb_name_selected = sc_sb_nameList[-1]

   sc_sb_country_dict = items_dict['sc_sb_country']
   sc_sb_countryList = sc_sb_country_dict['value'].split('::')
   sc_sb_country_selected = sc_sb_countryList[-1]

   sc_sb_city_dict = items_dict['sc_sb_city']
   sc_sb_cityList = sc_sb_city_dict['value'].split('::')
   sc_sb_city_selected = sc_sb_cityList[-1]

   sc_sb_state_dict = items_dict['sc_sb_state']
   sc_sb_stateList = sc_sb_state_dict['value'].split('::')
   sc_sb_state_selected = sc_sb_stateList[-1]

   sc_sb_zip_dict = items_dict['sc_sb_zip']
   sc_sb_zipList = sc_sb_zip_dict['value'].split('::')
   sc_sb_zip_selected = sc_sb_zipList[-1]

   sc_sb_address_1_dict = items_dict['sc_sb_address_1']
   sc_sb_address_1List = sc_sb_address_1_dict['value'].split('::')
   sc_sb_address_1_selected = sc_sb_address_1List[-1]

   sc_sb_address_2_dict = items_dict['sc_sb_address_2']
   sc_sb_address_2List = sc_sb_address_2_dict['value'].split('::')
   sc_sb_address_2_selected = sc_sb_address_2List[-1]

   sc_sd_name_dict = items_dict['sc_sd_name']
   sc_sd_nameList = sc_sd_name_dict['value'].split('::')
   sc_sd_name_selected = sc_sd_nameList[-1]

   
   sc_sd_country_dict = items_dict['sc_sd_country']
   sc_sd_countryList = sc_sd_country_dict['value'].split('::')
   sc_sd_country_selected = sc_sd_countryList[-1]
 
   sc_sd_city_dict = items_dict['sc_sd_city']
   sc_sd_cityList = sc_sd_city_dict['value'].split('::')
   sc_sd_city_selected = sc_sd_cityList[-1]

   sc_sd_state_dict = items_dict['sc_sd_city']
   sc_sd_stateList = sc_sd_state_dict['value'].split('::')
   sc_sd_state_selected = sc_sd_stateList[-1]

   sc_sd_zip_dict = items_dict['sc_sd_zip']
   sc_sd_zipList = sc_sd_zip_dict['value'].split('::')
   sc_sd_zip_selected = sc_sd_zipList[-1]


   sc_sd_address_1_dict = items_dict['sc_sd_address_1']
   sc_sd_address_1List = sc_sd_address_1_dict['value'].split('::')
   sc_sd_address_1_selected = sc_sd_address_1List[-1]
 
   sc_sd_address_2_dict = items_dict['sc_sd_address_2']
   sc_sd_address_2List = sc_sd_address_2_dict['value'].split('::')
   sc_sd_address_2_selected = sc_sd_address_2List[-1]

   sc_cl_name_dict = items_dict['sc_cl_name']
   sc_cl_nameList = sc_cl_name_dict['value'].split('::')
   sc_cl_name_selected = sc_cl_nameList[-1]

   sc_cl_phone_dict = items_dict['sc_cl_phone']
   sc_cl_phoneList = sc_cl_phone_dict['value'].split('::')
   sc_cl_phone_selected = sc_cl_phoneList[-1]

   sc_cl_website_dict = items_dict['sc_cl_website']
   sc_cl_websiteList = sc_cl_website_dict['value'].split('::')
   sc_cl_website_selected = sc_cl_websiteList[-1]


   sc_cl_notes_dict = items_dict['sc_cl_notes']
   sc_cl_notesList = sc_cl_notes_dict['value'].split('::')
   sc_cl_notes_selected = sc_cl_notesList[-1]

   sc_cl_captcha_dict = items_dict['sc_cl_captcha']
   sc_cl_captchaList = sc_cl_captcha_dict['value'].split('::')
   sc_cl_captcha_selected = sc_cl_captchaList[-1]

   sc_cl_terms_dict = items_dict['sc_cl_terms']
   sc_cl_termsList = sc_cl_terms_dict['value'].split('::')
   sc_cl_terms_selected = sc_cl_termsList[-1]

   showlabels= {'1': "No", '2': "Yes", '3' : "required"}
   items = {
   "sc_sb_name":showlabels[sc_sb_name_selected],
   "sc_sb_country":showlabels[sc_sb_country_selected],
   "sc_sb_city":showlabels[sc_sb_city_selected],
   "sc_sb_state":showlabels[sc_sb_state_selected],
   "sc_sb_zip":showlabels[sc_sb_zip_selected],
   "sc_sb_address_1":showlabels[sc_sb_address_1_selected],
   "sc_sb_address_2":showlabels[sc_sb_address_2_selected],

   "sc_sd_name":showlabels[sc_sd_name_selected],
   "sc_sd_country":showlabels[sc_sd_country_selected],
   "sc_sd_city":showlabels[sc_sd_city_selected],
   "sc_sd_state":showlabels[sc_sd_state_selected],
   "sc_sd_zip":showlabels[sc_sd_zip_selected],
   "sc_sd_address_1":showlabels[sc_sd_address_1_selected],
   "sc_sd_address_2":showlabels[sc_sd_address_2_selected],

    "sc_cl_name":showlabels[sc_cl_name_selected],
    "sc_cl_phone":showlabels[sc_cl_phone_selected],
    "sc_cl_website":showlabels[sc_cl_website_selected],
    "sc_cl_notes":showlabels[sc_cl_notes_selected],
    "sc_cl_captcha":showlabels[sc_cl_captcha_selected],
    "sc_cl_terms":showlabels[sc_cl_terms_selected],

   }
   return items;   