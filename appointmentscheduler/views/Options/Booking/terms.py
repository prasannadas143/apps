from django.shortcuts import render,get_object_or_404
from appointmentscheduler.models import AppschedulerOptions
import pdb,os
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage

tab_id = 9

def terms(request):

	if request.method == 'POST':
		o_terms_url = request.POST["o_terms_url"]
		o_terms_content = request.POST["o_terms_content"]
		item_url = get_object_or_404(AppschedulerOptions, key="o_terms_url")
		item_url.value = o_terms_url
		item_url.save()
		item_content = get_object_or_404(AppschedulerOptions, key="o_terms_content")
		item_content.value = o_terms_content
		item_content.save()
	items = AppschedulerOptions.objects.filter(tab_id=tab_id).values('key', 'value')
	items_dict = dict()
	for item in items:
		value = '' if item['value'] is None else item['value']
		items_dict[item['key']] = value
	template_name = "Options/Booking/terms.html"
	return render(request, template_name, {"terms" : items_dict})