from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from appointmentscheduler.models import AppschedulerOptions
from django.http import JsonResponse
import datetime, pdb
from django.views.decorators.csrf import requires_csrf_token, csrf_protect, csrf_exempt
from django.core import serializers
from PIL import Image
import io
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from base64 import decodestring
from django.http import JsonResponse
import datetime,pdb,os,json,re
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.forms.models import model_to_dict


def update_value(field_id, tab_id, newstep):
   item = AppschedulerOptions.objects.get(tab_id=int(tab_id), key = field_id)
   item.value = newstep;
   print(newstep);
   item.save()

@csrf_exempt
def Company(request):
	tab_id = 100;
	message=None
	Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)
	CompanyFormdata = dict()
	if request.method == 'POST':
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(field, tab_id , newstep.strip() )

	item = AppschedulerOptions.objects.filter(tab_id=tab_id)
	o_Website = item[10].value;
	o_Email = item[9].value;
	o_Fax = item[8].value;
	o_Phone = item[7].value;
	o_Zip = item[6].value;
	o_State = item[5].value;
	o_City = item[4].value;
	o_Country = item[3].value;
	o_StreetAddress = item[2].value;
	o_Name = item[1].value;
	o_CompanyName = item[0].value;

	items = {
	"o_CompanyName":o_CompanyName,
	"o_Name":o_Name,
    "o_StreetAddress":o_StreetAddress,
    "o_Country":o_Country,
    "o_City":o_City,
    "o_State":o_State,
    "o_Zip":o_Zip,
    "o_Phone":o_Phone,
    "o_Fax":o_Fax,
    "o_Email":o_Email,
    "o_Website":o_Website
	}
	CompanyFormdata['items'] = items
	# Then, do a redirect for example
	template_name="CompanyDetails.html"
	templatename=  os.path.join('Options','Invoice',template_name)
	return render(request,templatename, CompanyFormdata)