from django.shortcuts import render,get_object_or_404
from shoppingcart.options.models import  Options
import pdb,os
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


tab_id = 9

@requires_csrf_token
def terms(request):

	if request.method == 'POST':
		o_terms_url = request.POST["o_terms_url"]
		o_terms_content = request.POST["o_terms_content"]
		item_url = get_object_or_404(Options, key="o_terms_url",\
			app_name="shoppingcart")
		item_url.value = o_terms_url
		item_url.save()
		item_content = get_object_or_404(Options, \
			key="o_terms_content", app_name="shoppingcart")
		item_content.value = o_terms_content
		item_content.save()
		messages.success(request, 'Terms url and content are updated')

	items = Options.objects.filter(tab_id=tab_id, app_name="shoppingcart"\
		).values('key', 'value')
	items_dict = dict()
	for item in items:
		value = '' if item['value'] is None else item['value']
		items_dict[item['key']] = value
	templatename=  'terms.html'
	return render(request, templatename, {"terms" : items_dict})
