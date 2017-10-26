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
from django.views.decorators.csrf import requires_csrf_token, csrf_protect,csrf_exempt,requires_csrf_token
from django.forms.models import model_to_dict
from django.db.models.fields import DateField, TimeField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from appsplatform import settings

tab_id = 100;

def update_value(field_id, tab_id, newstep=''):
   item = AppschedulerOptions.objects.get(tab_id=int(tab_id), key = field_id)
   item.value = newstep;
   print(newstep);
   item.save()

@requires_csrf_token
def Company(request):
	message=None
	fs = FileSystemStorage()
	Options  = AppschedulerOptions.objects.all() # use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)

	CompanyFormdata = dict()
	if request.method == 'POST':
		request.POST._mutable = True
		del request.POST['csrfmiddlewaretoken']		
		companylogo = request.FILES['o_company_logo']
		item = AppschedulerOptions.objects.filter(tab_id=tab_id)
		companylogoname = item[11].value;
		uploaded_file_url = fs.url(companylogoname)
		if uploaded_file_url:
			oldimagepath=  os.path.join( settings.BASE_DIR, uploaded_file_url.lstrip('/') )
			if os.path.exists( oldimagepath ):
				os.remove(oldimagepath)

		filename = fs.save(companylogo.name, companylogo)
		request.POST['o_company_logo'] = filename
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(field, tab_id , newstep.strip() )

	item = AppschedulerOptions.objects.filter(tab_id=tab_id)
	companylogoname = item[11].value;
	uploaded_file_url = fs.url(companylogoname)

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
    "o_Website":o_Website,
    "o_company_logo" : uploaded_file_url
	}
	CompanyFormdata['items'] = items
	# Then, do a redirect for example
	template_name="CompanyDetails.html"
	templatename=  os.path.join('Options','Invoice',template_name)
	return render(request,templatename, CompanyFormdata)


def GetInvoiceCompanyvalues():
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
	"v_companyname":o_CompanyName,
	"v_name":o_Name,
    "v_streetaddress":o_StreetAddress,
    "v_country":o_Country,
    "v_city":o_City,
    "v_state":o_State,
    "v_zip":o_Zip,
    "v_phone":o_Phone,
    "v_fax":o_Fax,
    "v_email":o_Email,
    "v_website":o_Website
	}
	return items;

