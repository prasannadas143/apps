from django.shortcuts import render,get_object_or_404
from shoppingcart.options.models import  Options
import pdb,os
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
from appsplatform.settings.local import BASE_DIR
from PIL import Image

tab_id = 100;

def update_value(field_id, tab_id, newstep=''):
   item = get_object_or_404(Options,tab_id=int(tab_id), \
   	key = field_id,app_name="appointmentscheduler")
   item.value = newstep;
   print(newstep);
   item.save()

@requires_csrf_token
def Company(request):
	message=None
	template_name="CompanyDetails.html"
	fs = FileSystemStorage()
	# use filter() when you have sth to filter ;)
	# you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
	# you can remove the preview assignment (form =request.POST)

	CompanyFormdata = dict()
	if request.method == 'POST':
		request.POST._mutable = True
		del request.POST['csrfmiddlewaretoken']		
		companylogo = request.FILES['o_company_logo']
		try:
		    original = Image.open(companylogo)
		except:
			return render(request,templatename, {"error" : "Upload valid image"})
		item = Options.objects.filter(tab_id=tab_id)
		companylogoname = item[11].value;
		uploaded_file_url = fs.url(companylogoname)
		if uploaded_file_url:
			oldimagepath=  os.path.join( BASE_DIR, uploaded_file_url.lstrip('/') )
			if os.path.exists( oldimagepath ):
				os.remove(oldimagepath)

		filename = fs.save(companylogo.name, companylogo)
		request.POST['o_company_logo'] = filename
		for field in request.POST.keys():
			newstep = request.POST[field.strip()]
			update_value(field, tab_id , newstep.strip() )

	items = list(Options.objects.filter(tab_id=tab_id,app_name="appointmentscheduler"\
		).values('id','key', 'value'))
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item
	companylogoname = items_dict['o_company_logo']['value']
	if companylogoname:
		uploaded_file_url = fs.url(companylogoname)

	o_Website = items_dict['o_Website']['value']
	o_Email = items_dict['o_Email']['value']
	o_Fax = items_dict['o_Fax']['value']
	o_Phone = items_dict['o_Phone']['value']
	o_Zip = items_dict['o_Zip']['value']
	o_State = items_dict['o_State']['value']
	o_City = items_dict['o_City']['value']
	o_Country = items_dict['o_Country']['value']
	o_StreetAddress = items_dict['o_StreetAddress']['value']
	o_Name = items_dict['o_Name']['value']
	o_CompanyName = items_dict['o_CompanyName']['value']

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
	}
	if companylogoname:
		items['o_company_logo'] = uploaded_file_url

	CompanyFormdata['items'] = items
	# Then, do a redirect for example
	templatename=  os.path.join('Options','Invoice',template_name)
	return render(request,templatename, CompanyFormdata)


def GetInvoiceCompanyvalues():

	items = Options.objects.filter(tab_id=tab_id, app_name="appointmentscheduler"\
		).values('key', 'value')
	items_dict = dict()
	for item in items:
		items_dict[item['key']] = item
	companylogoname = items_dict['o_company_logo']['value']
	if companylogoname:
		uploaded_file_url = fs.url(companylogoname)

	o_Website = items_dict['o_Website']['value']
	o_Email = items_dict['o_Email']['value']
	o_Fax = items_dict['o_Fax']['value']
	o_Phone = items_dict['o_Phone']['value']
	o_Zip = items_dict['o_Zip']['value']
	o_State = items_dict['o_State']['value']
	o_City = items_dict['o_City']['value']
	o_Country = items_dict['o_Country']['value']
	o_StreetAddress = items_dict['o_StreetAddress']['value']
	o_Name = items_dict['o_Name']['value']
	o_CompanyName = items_dict['o_CompanyName']['value']

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
	}

	if companylogoname:
		items['o_company_logo'] = uploaded_file_url
	return items;

