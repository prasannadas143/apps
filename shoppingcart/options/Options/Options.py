from django.shortcuts import render,get_object_or_404
from ..models import  Options
from django.views.decorators.csrf import csrf_exempt

tab_id = 3

def update_value(field_id, tab_id, newstep):
   item =  get_object_or_404( Options,  tab_id=int(tab_id), id = int(field_id) )
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
   message=None
  # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   if request.method == 'POST':
      for field in request.POST.keys():
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
      message="opion is saved"
   items = Options.objects.filter(tab_id=tab_id).values('id','key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item

   ostep = items_dict['o_step']
   getsteps = ostep['value'].split('::')
   steps = getsteps[0].split('|')
   step_selected = getsteps[-1]
   step_id = ostep['id']

   ostatus_if_paid = items_dict['o_status_if_paid']
   status_if_paid = ostatus_if_paid['value'].split('::')
   status_if_paid_list = status_if_paid[0].split('|')
   status_if_paid_selected = status_if_paid[-1]
   status_id= ostatus_if_paid['id']
   
   ostatus_if_not_paid = items_dict['o_status_if_not_paid']
   status_if_not_paid = ostatus_if_not_paid['value'].split('::')
   status_if_not_paid_list = status_if_not_paid[0].split('|')
   status_if_not_paid_selected = status_if_not_paid[-1]
   status_not_id= ostatus_if_not_paid['id']

   ohide_prices = items_dict['o_hide_prices']
   hide_prices = ohide_prices['value'].split("::")
   hide_prices_list=hide_prices[0].split('|')
   hide_prices_list_selected=hide_prices[-1]
   hide_prices_id = ohide_prices['id']

   oaccept_booking_ahead = items_dict['o_accept_bookings_ahead']
   accept_booking_ahead = oaccept_booking_ahead['value'].split("::")
   accept_booking_ahead_list=accept_booking_ahead[0].split('|')
   accept_booking_ahead_selected=accept_booking_ahead[-1]
   accept_booking_ahead_id = oaccept_booking_ahead['id']

   oaccept_booking = items_dict['o_accept_bookings']
   accept_booking = oaccept_booking['value'].split("::")
   accept_booking_list=accept_booking[0].split('|')
   accept_booking_selected=accept_booking[-1]
   accept_booking_id = oaccept_booking['id']


   items = { "steps" : steps, "step_selected": step_selected,"status_if_paid_list":status_if_paid_list,
   "status_if_paid_selected":status_if_paid_selected,"status_if_not_paid_list":status_if_not_paid_list,
   "status_if_not_paid_selected":status_if_not_paid_selected,"hide_prices_list":hide_prices_list,
   "hide_prices_list_selected":hide_prices_list_selected.strip(),"accept_booking_list":accept_booking_list,
   "accept_booking_selected":accept_booking_selected.strip(), "step_id":  step_id, "status_id": status_id, "status_not_id": status_not_id,
   "accept_booking_ahead_selected" : accept_booking_ahead_selected.strip(),
   "hide_prices_id": hide_prices_id, "accept_booking_id" : accept_booking_id, "accept_booking_ahead_id" : accept_booking_ahead_id
   }
      # Then, do a redirect for example
   templatename=  'Options.html'

   return render(request,templatename, {'items':items ,"message":message })

def getbookingOptions():

   items = Options.objects.filter(tab_id=tab_id).values('key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item

   ostep = items_dict['o_step']
   getsteps = ostep['value'].split('::')
   steps = getsteps[0].split('|')
   step_selected = getsteps[-1]

   ostatus_if_paid = items_dict['o_status_if_paid']
   status_if_paid = ostatus_if_paid['value'].split('::')
   status_if_paid_list = status_if_paid[0].split('|')
   status_if_paid_selected = status_if_paid[-1]
   
   ostatus_if_not_paid = items_dict['o_status_if_not_paid']
   status_if_not_paid = ostatus_if_not_paid['value'].split('::')
   status_if_not_paid_list = status_if_not_paid[0].split('|')
   status_if_not_paid_selected = status_if_not_paid[-1]

   ohide_prices = items_dict['o_hide_prices']
   hide_prices = ohide_prices['value'].split("::")
   hide_prices_list=hide_prices[0].split('|')
   hide_prices_list_selected=hide_prices[-1]

   oaccept_booking_ahead = items_dict['o_accept_bookings_ahead']
   accept_booking_ahead = oaccept_booking_ahead['value'].split("::")
   accept_booking_ahead_list=accept_booking_ahead[0].split('|')
   accept_booking_ahead_selected=accept_booking_ahead[-1]

   oaccept_booking = items_dict['o_accept_bookings']
   accept_booking = oaccept_booking['value'].split("::")
   accept_booking_list=accept_booking[0].split('|')
   accept_booking_selected=accept_booking[-1]


   items = {  "STEP": step_selected,
      "STATUS_IF_PAID":status_if_paid_selected,
      "STATUS_IF_NOT_PAID":status_if_not_paid_selected,
      "ACCEPT_BOOKING_BEFORE_START":hide_prices_list_selected,
      "CANCEL_BOOKING_BEFORE_START":accept_booking_selected, 
      "ACCEPT_BOOKING_AHEAD" : accept_booking_ahead_selected,

      }

   return items

