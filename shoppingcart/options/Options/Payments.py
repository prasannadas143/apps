from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import requires_csrf_token,csrf_exempt
from django.contrib import messages
from shoppingcart.options.models import  Options
import pdb
from django.views.decorators.csrf import csrf_exempt

tab_id = 103;
def update_value(field_id, tab_id, newstep):
   item =  get_object_or_404( Options,  tab_id=int(tab_id), key = field_id )
   getsteps = item.value.split('::')
   if newstep == 'on':
      newstep = 1
   # get the user you want. (connect for example) in the var "user"
   if len(getsteps) == 2 :
      item.value = "{0}::{1}".format(getsteps[0], newstep )
   else :
      item.value = newstep 
   item.save()

@requires_csrf_token
def PaymentOptions(request):
   # pdb.set_trace()
   message=None
   # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   paymentdata = dict()
   if request.method == 'POST':
      request.POST._mutable = True
      if "sc_disable_payments_and_collect_orders" not in request.POST:
         request.POST["sc_disable_payments_and_collect_orders"] = 0
      if "sc_disable_order_and_enable_cart_catalogue" not in request.POST:
         request.POST["sc_disable_order_and_enable_cart_catalogue"] = 0
      for field in request.POST.keys():
         if field == 'csrfmiddlewaretoken':
            continue   
         newstep = request.POST[field.strip()]
         if isinstance(newstep, str) :
            newstep = newstep.strip()
         update_value(field, tab_id , newstep )
      messages.success(request, 'CheckoutForm options are updated.')
   items = Options.objects.filter(tab_id=tab_id).values('id','key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item
   #o_allow_authorize
   disable_payments_dict = items_dict['sc_disable_payments_and_collect_orders']
   disable_payments = disable_payments_dict['value'].split('::')
   disable_payments_list = disable_payments[0].split('|')
   disable_payments_selected = disable_payments[-1]
   disable_payments_id = disable_payments_dict['id']

   #o_deposit_type
   enable_cart_dict = items_dict['sc_disable_order_and_enable_cart_catalogue']
   enable_cart = enable_cart_dict['value'].split('::')
   enable_cart_list = enable_cart[0].split('|')
   enable_cart_selected = enable_cart[-1]
   enable_cart_id = enable_cart_dict['id']

   currency_dict = items_dict['sc_currency']
   currency = currency_dict['value'].split('::')
   currency_list = currency[0].split('|')
   currency_selected = currency[-1]
   currency_id = currency_dict['id']

   fee_type_dict = items_dict['sc_insurance_fee_type']
   fee_type = fee_type_dict['value'].split('::')
   fee_type_list = fee_type[0].split('|')
   fee_type_selected = fee_type[-1]
   fee_type_id = fee_type_dict['id']

   fee_dict = items_dict['sc_insurance_fee']
   fee = fee_dict['value']
   fee_id = fee_dict['id']

   items = { "disable_payments_list" : disable_payments_list, "disable_payments_selected": disable_payments_selected,
   "enable_cart_list":enable_cart_list, "enable_cart_selected":enable_cart_selected,
   "currency_list":currency_list,"currency_selected":currency_selected,
   "fee_type_list" : fee_type_list, "fee_type_selected" : fee_type_selected,
   "fee" : fee, "fee_id" : fee
   ,"disable_payments_id":disable_payments_id,"enable_cart_id":enable_cart_id,
   "currency_id":currency_id, "fee_type_id" : fee_type_id, "fee_id":fee_id
   }
   paymentdata['items'] = items
   # Then, do a redirect for example
   templatename=  'Payments.html'

   return render(request,templatename, paymentdata)

def getPaymentOptions():

   items = Options.objects.filter(tab_id=tab_id).values('id','key', 'value')
   items_dict = dict()

   for item in items:
      items_dict[item['key']] = item
   #o_allow_authorize
   disable_payments_dict = items_dict['sc_disable_payments_and_collect_orders']
   disable_payments = disable_payments_dict['value'].split('::')
   disable_payments_selected = disable_payments[-1]

   #o_deposit_type
   enable_cart_dict = items_dict['sc_disable_order_and_enable_cart_catalogue']
   enable_cart = enable_cart_dict['value'].split('::')
   enable_cart_selected = enable_cart[-1]

   currency_dict = items_dict['sc_currency']
   currency = currency_dict['value'].split('::')
   currency_selected = currency[-1]

   fee_type_dict = items_dict['sc_insurance_fee_type']
   fee_type = fee_type_dict['value'].split('::')
   fee_type_selected = fee_type[-1]

   fee_dict = items_dict['sc_insurance_fee']
   fee = fee_dict['value']
   fee_id = fee_dict['id']

   items = { "DISABLE_PAYMENTS_AND_COLLECT_ORDERS" : disable_payments_selected, 
   "DISABLE_ORDER_AND_ENABLE_CART_CATALOGUE":enable_cart_selected, 
   "CURRENCY":currency_selected,
   "INSURANCE_FEE_TYPE" : fee_type_selected, 
   "INSURANCE_FEE" : fee
   
   }
   return items
