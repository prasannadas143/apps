from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
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
from appointmentscheduler.form.Options.Editor.AddTemplate import addTemplate
from appointmentscheduler.form.Options.Editor.TemplateDetails import TemplateDetails, AppschedulerTemplatesDetails
from django.forms.models import model_to_dict
from appsplatform.settings import JSONFILES
from appointmentscheduler.models import  AppschedulerTemplates, AppschedulerCountries


@csrf_exempt
def EditorTemplate(request):
    template_name="ckEditor.html"
    templatename=  os.path.join('Options','Editor',template_name)
    Template_info = []
    Templates = AppschedulerTemplates.objects.all()
    for Templ in reversed(list(Templates)):
        data=dict()
        data['id'] = Templ.id
        data['templatename'] = Templ.TemplateName
        Template_info.append(data)
    return render(request, templatename, {"data" :  Template_info })


@csrf_exempt
def GetTemplateDetails(request):
    if request.method == "GET":
        Templates = AppschedulerTemplatesDetails.objects.filter(TemplateID=request.GET['TemplateID'])
        data=dict()
        if Templates.count()>0 :
            Template =Templates[0]
            data['id'] = Template.id
            data['TemplateID'] = Template.TemplateID
            data['subject'] = Template.subject
            data['DesignedTemplate'] = Template.DesignedTemplate
            data['status'] = Template.status
    return HttpResponse( json.dumps(data), content_type='application/json')

@csrf_exempt
def GetTemplateList(request):
    Templates = AppschedulerTemplates.objects.all()
    Template_info = []
    for Templ in reversed(list(Templates)):
        data=dict()
        data['id'] = Templ.id
        data['templatename'] = Templ.TemplateName
        Template_info.append(data)
    return  HttpResponse(json.dumps({"data" :Template_info }), content_type='application/json')

@csrf_exempt


def SaveTemplate(request):
    if request.method == 'POST': 
        appscheduleTemplate = TemplateDetails(request.POST or None)
        if appscheduleTemplate.is_valid():
            appscheduleTemplate.save()
    return HttpResponse(status=200)

@csrf_exempt
def UpdateTemplate(request,id=None):
    if request.method == 'POST':
        Templates = AppschedulerTemplatesDetails.objects.filter(id=id)[0]
        appscheduleTemplate = TemplateDetails(request.POST or None,instance=Templates)
        if appscheduleTemplate.is_valid():
            appscheduleTemplate.save()
        return HttpResponse(status=200)        

@csrf_exempt
def Template(request):      
	template_name="addTemplate.html"
	templatename=  os.path.join('Options','Editor',template_name)
	return render(request, templatename )


@csrf_exempt
def AddTemplate(request):
	if request.method == "POST":
			request.POST._mutable= True
			request.POST['status'] = bool(int(request.POST['Status']))
			appscheduleTemplate = addTemplate(request.POST or None)
			if appscheduleTemplate.is_valid():
				 	appscheduleTemplate.save()
	return HttpResponse(status=200)


@csrf_exempt
def CheckDuplicateTemplate(request):
	if request.method == "GET":
		Templates = AppschedulerTemplates.objects.filter(TemplateName=request.GET['TemplateName'])
		# DON'T USE
		if Templates.count() > 0  and Templates[0].TemplateName is not None:
			status = 1
		else :
			status = 0
	return HttpResponse(status, content_type='application/json')


@csrf_exempt
def Templates(request):
        template_name="TemplateList.html"
        templatename=  os.path.join('Options','Editor',template_name)
        return render(request, templatename ) 

@csrf_exempt
def deleteTemplate(request,id=None):
    aCountry=AppschedulerCountries.objects.get(id=id)
    pdb.set_trace()
    aCountry.delete()
    return HttpResponse(status=204)        
1
@csrf_exempt
def editTemplate(request,id):
    template_name="EditTemplate.html"
    appscheduleobj =AppschedulerTemplates.objects.get(id=id)
    appscheduleTemplate = addTemplate(request.POST or None ,instance=appscheduleobj)
    if appscheduleTemplate.is_valid():
        post = appscheduleTemplate.save()
        return HttpResponseRedirect('/appointmentschduler/Templates/')
    templatename=  os.path.join('Options','Editor',template_name)
    Templateinfo = model_to_dict(appscheduleobj)
    Templateinfo['status'] = int(Templateinfo['status'])
    return render(request,templatename, {'appscheduleTemplate': Templateinfo, "id" : id } )

@csrf_exempt
def TemplateList(request):
    Template_info=[]
    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "all":
            Template = AppschedulerTemplates.objects.all()
        elif querydata == "active":
            Template = AppschedulerTemplates.objects.filter(status = 1 )
        elif querydata == "inactive":
            Template = AppschedulerTemplates.objects.filter(status = 0 )
    else:
        Template = AppschedulerTemplates.objects.all()

    for Templ in reversed(list(Template)):
        data=dict()
        data['id'] = Templ.id
        data['TemplateName'] = Templ.TemplateName
        data['status'] = str(Templ.status)
        Template_info.append(data)
    return  HttpResponse(json.dumps({"data" :Template_info }), content_type='application/json')   



@csrf_exempt
def TemplateDetailsList(request):
        template_name="TemplateDetailsList.html"
        templatename=  os.path.join('Options','Editor',template_name)
        return render(request, templatename)


#Template details List
@csrf_exempt
def TemplateDetailsData(request):
    Template_info=[]
    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "all":
            Template = AppschedulerTemplatesDetails.objects.all()
        elif querydata == "active":
            Template = AppschedulerTemplatesDetails.objects.filter(status = 1 )
        elif querydata == "inactive":
            Template = AppschedulerTemplatesDetails.objects.filter(status = 0 )
    else:
        Template = AppschedulerTemplatesDetails.objects.all()

    for Templ in reversed(list(Template)):
        data=dict()
        print(Templ.id);
        data['id'] = Templ.id
        data['TemplateID'] = Templ.TemplateID
        data['TemplateName'] =  AppschedulerTemplates.objects.filter(id=Templ.TemplateID)[0].TemplateName
        data['subject'] = Templ.subject
        data['DesignedTemplate'] = Templ.DesignedTemplate
        data['status'] = str(Templ.status)
        Template_info.append(data)
    return  HttpResponse(json.dumps({"data" :Template_info }), content_type='application/json')



@csrf_exempt
def GetTemplateDetailByTemplateID(TemplateName=None):
    try:
        templates = AppschedulerTemplates.objects.filter(TemplateName__iexact=TemplateName.upper().strip())
        if len(templates) :
            templateid = templates[0].id
            Template = AppschedulerTemplatesDetails.objects.filter(TemplateID=templateid)[0]
    except Exception as e:
        print( '%s (%s)' % (e.message, type(e)) )
    return Template

