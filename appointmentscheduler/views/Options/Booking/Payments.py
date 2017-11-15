from django.shortcuts import render,get_object_or_404
from appointmentscheduler.models import  *
import pdb
from django.views.decorators.csrf import csrf_exempt

tab_id = 7;
def update_value(field_id, tab_id, newstep):
   item =  get_object_or_404( AppschedulerOptions,  tab_id=int(tab_id), id = int(field_id) )
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
   message=None
   # use filter() when you have sth to filter ;)
   # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
   # you can remove the preview assignment (form =request.POST)
   paymentdata = dict()
   if request.method == 'POST':
      for field in request.POST.keys():
         newstep = request.POST[field.strip()]
         update_value(field, tab_id , newstep.strip() )
      paymentdata['message'] ="opion is saved"

   items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('id','key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item
   #o_allow_authorize

   odisable_payments = items_dict['o_disable_payments']
   o_disable_paymentsList = odisable_payments['value'].split('::')
   o_disable_payments = o_disable_paymentsList[0].split('|')
   o_disable_payments_selected = o_disable_paymentsList[-1]
   o_disable_payments_id = odisable_payments['id']

   #o_deposit_type
   odeposit_type = items_dict['o_deposit_type']
   o_deposit_typeList =  odeposit_type['value'].split('::')
   o_deposit_type = o_deposit_typeList[0].split('|')
   o_deposit_type_selected = o_deposit_typeList[-1]
   o_deposit_type_id = odeposit_type['id']

   #o_deposit
   odeposit = items_dict['o_deposit']
   o_deposit = odeposit['value']
   o_deposit_id = odeposit['id']

   #o_tax
   otax = items_dict['o_tax']
   o_tax = otax['value']
   o_tax_id = otax['id']


   items = { "o_disable_paymentsList" : o_disable_paymentsList, "o_disable_payments_selected": o_disable_payments_selected,
   "o_deposit_typeList":o_deposit_type, "o_deposit_type_selected":o_deposit_type_selected,
   "o_deposit":o_deposit,"o_tax":o_tax,"o_disable_payments_id":o_disable_payments_id,"o_deposit_type_id":o_deposit_type_id,
   "o_deposit_id":o_deposit_id,"o_tax_id":o_tax_id
   }
   paymentdata['items'] = items
   # Then, do a redirect for example
   return render(request,'Payments.html', paymentdata)

def getPaymentOptions():

   items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('key', 'value')
   items_dict = dict()
   for item in items:
      items_dict[item['key']] = item
   #o_allow_authorize

   odisable_payments = items_dict['o_disable_payments']
   o_disable_paymentsList = odisable_payments['value'].split('::')
   o_disable_payments_selected = o_disable_paymentsList[-1]

   #o_deposit_type
   odeposit_type = items_dict['o_deposit_type']
   o_deposit_typeList =  odeposit_type['value'].split('::')
   o_deposit_type_selected = o_deposit_typeList[-1]

   #o_deposit
   odeposit = items_dict['o_deposit']
   o_deposit = odeposit['value']

   #o_tax
   otax = items_dict['o_tax']
   o_tax = otax['value']


   items = { "DISABLE_PAYMENTS": o_disable_payments_selected,
    "DEPOSIT_TYPE":o_deposit_type_selected,
   "DEPOSIT":o_deposit,"TAX":o_tax
   }
   return items
