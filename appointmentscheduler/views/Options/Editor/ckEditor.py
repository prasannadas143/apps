from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from appointmentscheduler.models import AppschedulerCountries
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
#from  appointmentscheduler.form.Options.ckEditor.ckEditor import ckEditor
from django.forms.models import model_to_dict


@csrf_exempt
def EditorTemplate(request):
        template_name="ckEditor.html"
        templatename=  os.path.join('Options','Editor',template_name)
        return render(request, templatename ) 

@csrf_exempt
def SaveTemplate(request):
		if request.method == 'POST':
			TemplateData = request.POST['TemplateData']
			return HttpResponse(status=200)
   