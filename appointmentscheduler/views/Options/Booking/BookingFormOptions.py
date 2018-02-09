from django.shortcuts import render
from appointmentscheduler.models import  *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  get_object_or_404


tab_id = 4;

def update_value(field_id, tab_id, newstep):
   item =   get_object_or_404( AppschedulerOptions,  tab_id=int(tab_id), id = int(field_id) )
   getsteps = item.value.split('::')
   # get the user you want. (connect for example) in the var "user"
   if len(getsteps) >1 :
      item.value = "{0}::{1}".format(getsteps[0], newstep )
   else :
      item.value = newstep ;
   item.save()

@csrf_exempt
def BookingFormOptions(request):
   message=None
   # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   BookingFormdata = dict()
   if request.method == 'POST':
      for field in request.POST.keys():
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
         BookingFormdata['message'] ="Booking opion is saved"

   items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('id','key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item

   obf_zip = items_dict['o_bf_zip']
   o_bf_zipList = obf_zip['value'].split('::')
   o_bf_zip = o_bf_zipList[0].split('|')
   o_bf_zip_selected = o_bf_zipList[-1]
   o_bf_zip_id = obf_zip['id']

   obf_terms = items_dict['o_bf_terms']
   o_bf_termsList = obf_terms['value'].split('::')
   o_bf_terms = o_bf_termsList[0].split('|')
   o_bf_terms_selected = o_bf_termsList[-1]
   o_bf_terms_id = obf_terms['id']

   obf_states = items_dict['o_bf_state']
   o_bf_stateList = obf_states['value'].split('::')
   o_bf_state = o_bf_stateList[0].split('|')
   o_bf_state_selected = o_bf_stateList[-1]
   o_bf_state_id = obf_states['id']

   obf_phone = items_dict['o_bf_phone']
   o_bf_phoneList = obf_phone['value'].split('::')
   o_bf_phone = o_bf_phoneList[0].split('|')
   o_bf_phone_selected = o_bf_phoneList[-1]
   o_bf_phone_id = obf_phone['id']

   obf_notes = items_dict['o_bf_notes']
   o_bf_notesList = obf_notes['value'].split('::')
   o_bf_notes = o_bf_phoneList[0].split('|')
   o_bf_notes_selected = o_bf_phoneList[-1]
   o_bf_notes_id = obf_notes['id']
  
   obf_name = items_dict['o_bf_name']
   o_bf_nameList = obf_name['value'].split('::')
   o_bf_name = o_bf_nameList[0].split('|')
   o_bf_name_selected = o_bf_nameList[-1]
   o_bf_name_id = obf_name['id']

   obf_email = items_dict['o_bf_email']
   o_bf_emailList = obf_email['value'].split('::')
   o_bf_email = o_bf_emailList[0].split('|')
   o_bf_email_selected = o_bf_emailList[-1]
   o_bf_email_id = obf_email['id']

   obf_country = items_dict['o_bf_country']
   o_bf_countryList = obf_country['value'].split('::')
   o_bf_country = o_bf_emailList[0].split('|')
   o_bf_country_selected = o_bf_emailList[-1]
   o_bf_country_id = obf_country['id']
   
   obf_city = items_dict['o_bf_city']
   o_bf_cityList = obf_city['value'].split('::')
   o_bf_city = o_bf_cityList[0].split('|')
   o_bf_city_selected = o_bf_cityList[-1]
   o_bf_city_id = obf_city['id']

   obf_captcha = items_dict['o_bf_captcha']
   o_bf_captchaList = obf_captcha['value'].split('::')
   o_bf_captcha = o_bf_captchaList[0].split('|')
   o_bf_captcha_selected = o_bf_captchaList[-1]
   o_bf_captcha_id = obf_captcha['id']

   obf_address_2 = items_dict['o_bf_address_2']
   o_bf_address_2List = obf_address_2['value'].split('::')
   o_bf_address_2 = o_bf_cityList[0].split('|')
   o_bf_address_2_selected = o_bf_cityList[-1]
   o_bf_address_2_id = obf_address_2['id']

   obf_address_1 = items_dict['o_bf_address_1']
   o_bf_address_1List = obf_address_1['value'].split('::')
   o_bf_address_1 = o_bf_address_1List[0].split('|')
   o_bf_address_1_selected = o_bf_address_1List[-1]
   o_bf_address_1_id = obf_address_1['id']
 
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
   templatename=  os.path.join('Options','Booking','BookingForm.html')

   return render(request,templatename, BookingFormdata)



def GetBookingValidation():
  
   items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item

   obf_zip = items_dict['o_bf_zip']
   o_bf_zipList = obf_zip['value'].split('::')
   o_bf_zip = o_bf_zipList[0].split('|')
   o_bf_zip_selected = o_bf_zipList[-1]

   obf_terms = items_dict['o_bf_terms']
   o_bf_termsList = obf_terms['value'].split('::')
   o_bf_terms = o_bf_termsList[0].split('|')
   o_bf_terms_selected = o_bf_termsList[-1]

   obf_states = items_dict['o_bf_state']
   o_bf_stateList = obf_states['value'].split('::')
   o_bf_state = o_bf_stateList[0].split('|')
   o_bf_state_selected = o_bf_stateList[-1]

   obf_phone = items_dict['o_bf_phone']
   o_bf_phoneList = obf_phone['value'].split('::')
   o_bf_phone = o_bf_phoneList[0].split('|')
   o_bf_phone_selected = o_bf_phoneList[-1]

   obf_notes = items_dict['o_bf_notes']
   o_bf_notesList = obf_notes['value'].split('::')
   o_bf_notes = o_bf_phoneList[0].split('|')
   o_bf_notes_selected = o_bf_phoneList[-1]
  
   obf_name = items_dict['o_bf_name']
   o_bf_nameList = obf_name['value'].split('::')
   o_bf_name = o_bf_nameList[0].split('|')
   o_bf_name_selected = o_bf_nameList[-1]

   obf_email = items_dict['o_bf_email']
   o_bf_emailList = obf_email['value'].split('::')
   o_bf_email = o_bf_emailList[0].split('|')
   o_bf_email_selected = o_bf_emailList[-1]

   obf_country = items_dict['o_bf_country']
   o_bf_countryList = obf_country['value'].split('::')
   o_bf_country = o_bf_emailList[0].split('|')
   o_bf_country_selected = o_bf_emailList[-1]
   
   obf_city = items_dict['o_bf_city']
   o_bf_cityList = obf_city['value'].split('::')
   o_bf_city = o_bf_cityList[0].split('|')
   o_bf_city_selected = o_bf_cityList[-1]

   obf_captcha = items_dict['o_bf_captcha']
   o_bf_captchaList = obf_captcha['value'].split('::')
   o_bf_captcha = o_bf_captchaList[0].split('|')
   o_bf_captcha_selected = o_bf_captchaList[-1]

   obf_address_2 = items_dict['o_bf_address_2']
   o_bf_address_2List = obf_address_2['value'].split('::')
   o_bf_address_2 = o_bf_cityList[0].split('|')
   o_bf_address_2_selected = o_bf_cityList[-1]

   obf_address_1 = items_dict['o_bf_address_1']
   o_bf_address_1List = obf_address_1['value'].split('::')
   o_bf_address_1 = o_bf_address_1List[0].split('|')
   o_bf_address_1_selected = o_bf_address_1List[-1]

   showlabels= {'1': "No", '2': "Yes", '3' : "required"}
   items = {"c_zip":showlabels[o_bf_zip_selected],
   "c_state":showlabels[o_bf_state_selected],"c_phone":showlabels[o_bf_phone_selected],
   "c_notes":showlabels[o_bf_notes_selected],"c_name":showlabels[o_bf_name_selected],
   "c_email":showlabels[o_bf_email_selected],

   "c_country":showlabels[o_bf_country_selected],"c_city":showlabels[o_bf_city_selected],
   "c_address_2":showlabels[o_bf_address_2_selected],
   "c_address_1":showlabels[o_bf_address_1_selected]
   }
   #,"c_terms":o_bf_terms_selected, "c_captcha":showlabels[o_bf_captcha_selected], 
   return items;   