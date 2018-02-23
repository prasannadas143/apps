from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,  get_object_or_404
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from django.forms.models import model_to_dict
import json
from .form import FormTemplate,FormTemplateDetails
from .models import  SmsEmailTemplates, SmsEmailTemplatesDetails




@ensure_csrf_cookie
def GetTemplateList(request):
    templates = SmsEmailTemplates.objects.all().order_by('-id')
    template_info = []
    for templ in templates.iterator():
        data=dict()
        data['id'] = templ.id
        data['templatename'] = templ.TemplateName
        template_info.append(data)
    return  HttpResponse(json.dumps({"data" :template_info }), content_type='application/json')

@ensure_csrf_cookie
def SaveTemplate(request):
	if request.method == 'POST': 
		form_template = FormTemplate(request.POST or None)
		if form_template.is_valid():
		    form_template.save()
		    return HttpResponse(status=200)
		else :
		    return HttpResponse(status=404)
# @csrf_exempt
# def UpdateTemplate(request,id=None):
#     if request.method == 'POST':
#         Templates = AppschedulerTemplatesDetails.objects.filter(id=id)[0]
#         appscheduleTemplate = TemplateDetails(request.POST or None,instance=Templates)
#         if appscheduleTemplate.is_valid():
#             appscheduleTemplate.save()
#         return HttpResponse(status=200)        

@requires_csrf_token
def Template(request):      
	templatename="addTemplate.html"
	return render(request, templatename )


@ensure_csrf_cookie
def AddTemplate(request):
    if request.method == "POST":
        request.POST._mutable= True
        templateform = FormTemplate(request.POST or None)
        if templateform.is_valid():
            templateform.save()
            return HttpResponse(status=200)
        else :
            return HttpResponse(status=404)


@ensure_csrf_cookie
def CheckDuplicateTemplate(request):
	if request.method == "GET":
		templates = SmsEmailTemplates.objects.filter(TemplateName=request.GET['TemplateName'])
		# DON'T USE
		if templates.count() > 0  and templates[0].TemplateName is not None:
			status = 1
		else :
			status = 0
	return HttpResponse(status, content_type='application/json')



@ensure_csrf_cookie
def deleteTemplate(request,id=None):
    atemplate=get_object_or_404(SmsEmailTemplates,id=int(id))
    atemplate.delete()
    templatedetail = SmsEmailTemplatesDetails.objects.filter(TemplateID=int(id))
    # DON'T USE
    if templatedetail.exists():
        templatedetail[0].delete()
    return HttpResponse(status=204)       

@ensure_csrf_cookie
def deleteTemplates(request,rowids=None):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        atemplate=get_object_or_404(SmsEmailTemplates,id=int(id))
        atemplate.delete()
        templatedetail = SmsEmailTemplatesDetails.objects.filter(TemplateID=int(id))
        # DON'T USE
        if templatedetail.exists():
            templatedetail[0].delete()
    return HttpResponse(status=204)        

@ensure_csrf_cookie
def editTemplate(request,id):
    templatename="EditTemplate.html"
    templateobj =get_object_or_404(SmsEmailTemplates,id=int(id))
    formtemplate = FormTemplate(request.POST or None ,instance=templateobj)
    if request.method == "POST":
        if formtemplate.is_valid():
            post = formtemplate.save()
            return HttpResponse(status=204) 
        else :
            return HttpResponse(status=404) 
  
    templateinfo = model_to_dict(templateobj)
    return render(request,templatename, {'appscheduleTemplate': \
    	templateinfo, "id" : id } )

@ensure_csrf_cookie
def TemplateList(request):
    template_info=[]
    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "all":
            templates = SmsEmailTemplates.objects.all().order_by('-id')
        elif querydata == "active":
            templates = SmsEmailTemplates.objects.filter(status = 1 ).order_by('-id')
        elif querydata == "inactive":
            templates = SmsEmailTemplates.objects.filter(status = 0 ).order_by('-id')
    else:
        templates = SmsEmailTemplates.objects.all().order_by('-id')

    for templ in templates.iterator():
        data=dict()
        data['id'] = templ.id
        data['TemplateName'] = templ.TemplateName
        template_info.append(data)
    return  HttpResponse(json.dumps({"data" :template_info }), content_type='application/json')   



@requires_csrf_token
def TemplateDetailsData(request):
    template_info=[]
    if 'querydata' in request.GET:
        querydata = request.GET['querydata']
        if querydata == "all":
            templates = SmsEmailTemplatesDetails.objects.all().order_by('-id')
        elif querydata == "active":
            templates = SmsEmailTemplatesDetails.objects.filter(status = 1 ).order_by('-id')
        elif querydata == "inactive":
            templates = SmsEmailTemplatesDetails.objects.filter(status = 0 ).order_by('-id')
    else:
        templates = SmsEmailTemplatesDetails.objects.all().order_by('-id')

    for templ in templates.iterator():
        data=dict()
        print(templ.id);
        data['id'] = templ.id
        data['TemplateID'] = templ.TemplateID
        data['TemplateName'] =   get_object_or_404(SmsEmailTemplates,id=templ.TemplateID).TemplateName
        data['subject'] = templ.subject
        data['DesignedTemplate'] = templ.DesignedTemplate
        template_info.append(data)
    return  HttpResponse(json.dumps({"data" :template_info }), content_type='application/json')

@ensure_csrf_cookie
def GetTemplateDetails(request):
    """ Retrieve all template details with it's subject"""
    if request.method == "GET":
        templates = SmsEmailTemplatesDetails.objects.filter(TemplateID=request.GET['TemplateID'])
        data=dict()
        if templates.exists() :
            template =templates[0]
            data['id'] = template.id
            data['TemplateID'] = template.TemplateID
            data['subject'] = template.subject
            data['DesignedTemplate'] = template.DesignedTemplate
    return HttpResponse( json.dumps(data), content_type='application/json')


def GetTemplateDetailByTemplateID(TemplateName=None):
    template = None
    try:
   
        templates = SmsEmailTemplates.objects.filter(TemplateName__iexact=TemplateName.upper().strip())
        if templates.exists() :
           
            templateid = templates[0].id
            template_dtls = SmsEmailTemplatesDetails.objects.filter(TemplateID=templateid)
            if template_dtls.exists() :
                template = template_dtls[0]
    except Exception as e:
        print( '%s (%s)' % (str(e), type(e)) )
    return template

@requires_csrf_token
def EditorTemplate(request):
    templatename="EditEditorTemplate.html"
    template_info = []
    templates = SmsEmailTemplates.objects.all()
    for templ in templates.iterator():
        data=dict()
        data['id'] = templ.id
        data['templatename'] = templ.TemplateName
        template_info.append(data)
    return render(request, templatename, {"listtemplates" :  \
    	template_info })

  


@requires_csrf_token
def EditEditorTemplate(request,id):
    templatename="EditEditorTemplate.html"
    editortemplateobj =get_object_or_404(SmsEmailTemplatesDetails,id=int(id))
    # appscheduleTemplate = addTemplate(request.POST or None ,instance=editortemplateobj)
    # if appscheduleTemplate.is_valid():
    #     post = appscheduleTemplate.save()
    #     return HttpResponseRedirect('/appointmentschduler/Templates/')
    list_template = []
    templates = SmsEmailTemplates.objects.all()
    for templ in templates.iterator():
        data=dict()
        data['id'] = templ.id
        data['templatename'] = templ.TemplateName
        list_template.append(data)
    templateinfo = model_to_dict(editortemplateobj)
    templateinfo['TemplateID'] =int(templateinfo['TemplateID'])
    return render(request,templatename, {'listtemplates': \
        list_template, "templateinfo" : templateinfo, "id" : id } )

@requires_csrf_token
def SaveEditorTemplate(request):
    templatename="EditEditorTemplate.html"
    template_editor_id,template_id = None,None
   
    if 'TemplateID' in request.POST:
        template_id = request.POST['TemplateID']

    list_template = []
    templates = SmsEmailTemplates.objects.all()
    for templ in templates.iterator():
        data=dict()
        data['id'] = templ.id
        data['templatename'] = templ.TemplateName
        list_template.append(data)
    templatedetail = None
    if template_id :
        templatedetail = SmsEmailTemplatesDetails.objects.filter( \
        TemplateID=int(template_id) )
    if templatedetail and templatedetail.exists() :
        #Edit the template

        if request.POST:
            templatedetailform = FormTemplateDetails(request.POST or \
                None ,instance=templatedetail[0])
    else :
        # Add the template
        if request.POST:
            templatedetailform = FormTemplateDetails(request.POST or \
                None )

    if request.POST :
        if  templatedetailform.is_valid():
            templatedetailform.save()
            messages.success(request, 'Template details are updated.')
            templateinfo =get_object_or_404(SmsEmailTemplatesDetails,
        TemplateID=int(template_id) )
        else :
            return render(request,templatename, \
                {'appscheduletemplate': templatedetailform, \
                "id" : template_id } )
    
    templateinfo.TemplateID =int(templateinfo.TemplateID)
       
    return render(request,templatename, {'templateinfo': \
        templateinfo, "id" : template_id ,"listtemplates" : list_template } )

@ensure_csrf_cookie
def DeleteEditorTemplate(request, id=None):
    template_instace = get_object_or_404(SmsEmailTemplatesDetails,id=int(id))
    template_instace.delete()
    return HttpResponse(status=204)  

@ensure_csrf_cookie
def DeleteEditorTemplates(request,rowids=None):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        atemplate=get_object_or_404(SmsEmailTemplatesDetails,id=int(id))
        atemplate.delete()
    return HttpResponse(status=204) 