from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
import pdb,os,json
from django.views.decorators.csrf import csrf_exempt
from appointmentscheduler.form.Options.Editor.AddTemplate import addTemplate
from appointmentscheduler.form.Options.Editor.TemplateDetails import TemplateDetails, AppschedulerTemplatesDetails
from django.forms.models import model_to_dict
from appointmentscheduler.models import  AppschedulerTemplates, AppschedulerCountries



@csrf_exempt
def EditorTemplate(request):
    template_name="ckEditor.html"
    templatename=  os.path.join('Options','Editor',template_name)
    Template_info = []
    Templates = AppschedulerTemplates.objects.all()
    for Templ in Templates.iterator():
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
        if Templates.exists() :
            Template =Templates[0]
            data['id'] = Template.id
            data['TemplateID'] = Template.TemplateID
            data['subject'] = Template.subject
            data['DesignedTemplate'] = Template.DesignedTemplate
            data['status'] = Template.status
    return HttpResponse( json.dumps(data), content_type='application/json')

@csrf_exempt
def GetTemplateList(request):
    Templates = AppschedulerTemplates.objects.all().order_by('-id')
    Template_info = []
    for Templ in Templates.iterator():
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
    atemplate=get_object_or_404(AppschedulerTemplates,id=id)
    atemplate.delete()
    return HttpResponse(status=204)        

@csrf_exempt
def editTemplate(request,id):
    template_name="EditTemplate.html"
    appscheduleobj =get_object_or_404(AppschedulerTemplates,id=id)
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
            Template = AppschedulerTemplates.objects.all().order_by('-id')
        elif querydata == "active":
            Template = AppschedulerTemplates.objects.filter(status = 1 ).order_by('-id')
        elif querydata == "inactive":
            Template = AppschedulerTemplates.objects.filter(status = 0 ).order_by('-id')
    else:
        Template = AppschedulerTemplates.objects.all().order_by('-id')

    for Templ in Template.iterator():
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
            Template = AppschedulerTemplatesDetails.objects.all().order_by('-id')
        elif querydata == "active":
            Template = AppschedulerTemplatesDetails.objects.filter(status = 1 ).order_by('-id')
        elif querydata == "inactive":
            Template = AppschedulerTemplatesDetails.objects.filter(status = 0 ).order_by('-id')
    else:
        Template = AppschedulerTemplatesDetails.objects.all().order_by('-id')

    for Templ in Template.iterator():
        data=dict()
        print(Templ.id);
        data['id'] = Templ.id
        data['TemplateID'] = Templ.TemplateID
        data['TemplateName'] =   get_object_or_404(AppschedulerTemplates,id=Templ.TemplateID).TemplateName
        data['subject'] = Templ.subject
        data['DesignedTemplate'] = Templ.DesignedTemplate
        data['status'] = str(Templ.status)
        Template_info.append(data)
    return  HttpResponse(json.dumps({"data" :Template_info }), content_type='application/json')



@csrf_exempt
def GetTemplateDetailByTemplateID(TemplateName=None):
    Template = None
    try:
   
        templates = AppschedulerTemplates.objects.filter(TemplateName__iexact=TemplateName.upper().strip())
        if templates.exists() :
           
            templateid = templates[0].id
            template_dtls = AppschedulerTemplatesDetails.objects.filter(TemplateID=templateid)
            if template_dtls.exists() :
                Template = template_dtls[0]
    except Exception as e:
        print( '%s (%s)' % (str(e), type(e)) )
    return Template

