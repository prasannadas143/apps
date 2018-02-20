from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
import pdb,os,json
from django.views.decorators.csrf import requires_csrf_token,\
csrf_protect,csrf_exempt,ensure_csrf_cookie
from appointmentscheduler.form.Options.Editor.AddTemplate import addTemplate
from appointmentscheduler.form.Options.Editor.TemplateDetails import TemplateDetails
from django.forms.models import model_to_dict
from appointmentscheduler.models import  AppschedulerTemplates,\
 AppschedulerCountries, AppschedulerTemplatesDetails




@ensure_csrf_cookie
def GetTemplateList(request):
    Templates = AppschedulerTemplates.objects.all().order_by('-id')
    Template_info = []
    for Templ in Templates.iterator():
        data=dict()
        data['id'] = Templ.id
        data['templatename'] = Templ.TemplateName
        Template_info.append(data)
    return  HttpResponse(json.dumps({"data" :Template_info }), content_type='application/json')

@ensure_csrf_cookie
def SaveTemplate(request):
    if request.method == 'POST': 
        appscheduleTemplate = addTemplate(request.POST or None)
        if appscheduleTemplate.is_valid():
            appscheduleTemplate.save()
            return HttpResponse(status=200)

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
	template_name="addTemplate.html"
	templatename=  os.path.join('Options','Editor',template_name)
	return render(request, templatename )


@ensure_csrf_cookie
def AddTemplate(request):
    if request.method == "POST":
        request.POST._mutable= True
        request.POST['status'] = bool(int(request.POST['Status']))
        appscheduleTemplate = addTemplate(request.POST or None)
        if appscheduleTemplate.is_valid():
            appscheduleTemplate.save()
            return HttpResponse(status=200)
        else :
            return HttpResponse(status=404)


@ensure_csrf_cookie
def CheckDuplicateTemplate(request):
	if request.method == "GET":
		Templates = AppschedulerTemplates.objects.filter(TemplateName=request.GET['TemplateName'])
		# DON'T USE
		if Templates.count() > 0  and Templates[0].TemplateName is not None:
			status = 1
		else :
			status = 0
	return HttpResponse(status, content_type='application/json')


@requires_csrf_token
def Templates(request):
        template_name="TemplateList.html"
        templatename=  os.path.join('Options','Editor',template_name)
        return render(request, templatename ) 

@ensure_csrf_cookie
def deleteTemplate(request,id=None):
    atemplate=get_object_or_404(AppschedulerTemplates,id=int(id))
    atemplate.delete()
    templatedetail = AppschedulerTemplatesDetails.objects.filter(TemplateID=int(id))
    # DON'T USE
    if templatedetail.exists():
        templatedetail.delete()
    return HttpResponse(status=204)       

@ensure_csrf_cookie
def deleteTemplates(request,rowids=None):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        atemplate=get_object_or_404(AppschedulerTemplates,id=int(id))
        atemplate.delete()
        templatedetail = AppschedulerTemplatesDetails.objects.filter(TemplateID=int(id))
        # DON'T USE
        if templatedetail.exists():
            templatedetail.delete()
    return HttpResponse(status=204)        

@ensure_csrf_cookie
def editTemplate(request,id):
    template_name="EditTemplate.html"
    appscheduleobj =get_object_or_404(AppschedulerTemplates,id=id)
    appscheduleTemplate = addTemplate(request.POST or None ,instance=appscheduleobj)
    if request.method == "POST":
        if appscheduleTemplate.is_valid():
            post = appscheduleTemplate.save()
            return HttpResponse(status=204) 
        else :
            return HttpResponse(status=404) 
  
    templatename=  os.path.join('Options','Editor',template_name)
    Templateinfo = model_to_dict(appscheduleobj)
    Templateinfo['status'] = int(Templateinfo['status'])
    return render(request,templatename, {'appscheduleTemplate': Templateinfo, "id" : id } )

@ensure_csrf_cookie
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



@requires_csrf_token
def TemplateDetailsList(request):
        template_name="TemplateDetailsList.html"
        templatename=  os.path.join('Options','Editor',template_name)
        return render(request, templatename)


#Template details List
@requires_csrf_token
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

@ensure_csrf_cookie
def GetTemplateDetails(request):
    """ Retrieve all template details with it's subject"""
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

@requires_csrf_token
def EditorTemplate(request):
    template_name="EditEditorTemplate.html"
    templatename=  os.path.join('Options','Editor',template_name)
    Template_info = []
    Templates = AppschedulerTemplates.objects.all()
    for Templ in Templates.iterator():
        data=dict()
        data['id'] = Templ.id
        data['templatename'] = Templ.TemplateName
        Template_info.append(data)
    return render(request, templatename, {"listtemplates" :  Template_info })

  


@requires_csrf_token
def EditEditorTemplate(request,id):
    template_name="EditEditorTemplate.html"
    editortemplateobj =get_object_or_404(AppschedulerTemplatesDetails,id=int(id))
    # appscheduleTemplate = addTemplate(request.POST or None ,instance=editortemplateobj)
    # if appscheduleTemplate.is_valid():
    #     post = appscheduleTemplate.save()
    #     return HttpResponseRedirect('/appointmentschduler/Templates/')
    list_template = []
    Templates = AppschedulerTemplates.objects.all()
    for Templ in Templates.iterator():
        data=dict()
        data['id'] = Templ.id
        data['templatename'] = Templ.TemplateName
        list_template.append(data)
    templatename=  os.path.join('Options','Editor',template_name)
    Templateinfo = model_to_dict(editortemplateobj)
    Templateinfo['TemplateID'] =int(Templateinfo['TemplateID'])
    return render(request,templatename, {'listtemplates': \
        list_template, "templateinfo" : Templateinfo, "id" : id } )

@requires_csrf_token
def SaveEditorTemplate(request):
    template_name="EditEditorTemplate.html"
    templatename=  os.path.join('Options','Editor',template_name)
    template_editor_id,template_id = None,None
   
    if 'TemplateID' in request.POST:
        template_id = request.POST['TemplateID']

    list_template = []
    Templates = AppschedulerTemplates.objects.all()
    for Templ in Templates.iterator():
        data=dict()
        data['id'] = Templ.id
        data['templatename'] = Templ.TemplateName
        list_template.append(data)
    apptemplatedetail = None
    if template_id :
        apptemplatedetail =AppschedulerTemplatesDetails.objects.filter( \
        TemplateID=int(template_id) )
    if apptemplatedetail and apptemplatedetail.exists() :
        #Edit the template

        if request.POST:
            apptemplatedetailform = TemplateDetails(request.POST or \
                None ,instance=apptemplatedetail[0])
    else :
        # Add the template
        if request.POST:
            apptemplatedetailform = TemplateDetails(request.POST or \
                None )

    if request.POST :
        if  apptemplatedetailform.is_valid():
            apptemplatedetailform.save()
            messages.success(request, 'Template details are updated.')
            Templateinfo =get_object_or_404(AppschedulerTemplatesDetails,
        TemplateID=int(template_id) )
        else :
            return render(request,templatename, \
                {'appscheduletemplate': apptemplatedetailform, \
                "id" : template_id } )
    
    Templateinfo.TemplateID =int(Templateinfo.TemplateID)
       
    return render(request,templatename, {'templateinfo': \
        Templateinfo, "id" : template_id ,"listtemplates" : list_template } )

@ensure_csrf_cookie
def DeleteEditorTemplate(request, id=None):
    Template = None
    template_instace = get_object_or_404(AppschedulerTemplatesDetails,id=int(id))
    template_instace.delete()
    return HttpResponse(status=204)  

@ensure_csrf_cookie
def DeleteEditorTemplates(request,rowids=None):
    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        atemplate=get_object_or_404(AppschedulerTemplatesDetails,id=int(id))
        atemplate.delete()
    return HttpResponse(status=204) 