from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from . import views as ckEditor

urlpatterns = [
    url(r'^Templates/$', TemplateView.as_view(template_name='TemplateList.html'), name="Templates"),
    url(r'^TemplateList/$', ckEditor.TemplateList, name="TemplateList"),
    url(r'^AddTemplate/$', ckEditor.AddTemplate, name="AddTemplate"),
    url(r'^SaveTemplate/$', ckEditor.SaveTemplate, name="SaveTemplate"),
    url(r'^editTemplate/(?P<id>\d+)/$', ckEditor.editTemplate, name="UpdateTemplate"),
    url(r'^Template/$', TemplateView.as_view(template_name='addTemplate.html'), name="Template"),
    url(r'^deleteTemplate/(?P<id>\d+)/$', ckEditor.deleteTemplate, name="deleteTemplate"),
    url(r'^deleteTemplates/$', ckEditor.deleteTemplates, name="deleteTemplates"),

    url(r'^EditorTemplate/$', ckEditor.EditorTemplate, name="EditorTemplate"),
    url(r'^CheckDuplicateTemplate/$', ckEditor.CheckDuplicateTemplate, name="CheckDuplicateTemplate"),
    url(r'^EditEditorTemplate/(?P<id>\d+)/$', ckEditor.EditEditorTemplate, name="EditEditorTemplate"),
    url(r'^GetTemplateDetails/$', ckEditor.GetTemplateDetails, name="GetTemplateDetails"),
    url(r'^TemplateDetailsList/$', TemplateView.as_view(template_name='TemplateDetailsList.html'), name="TemplateDetailsList"),
    url(r'^TemplateDetailsData/$', ckEditor.TemplateDetailsData, name="TemplateDetailsData"),
    url(r'^DeleteEditorTemplate/(?P<id>\d+)/$', ckEditor.DeleteEditorTemplate, name="DeleteEditorTemplate"),
    url(r'^DeleteEditorTemplates/$', ckEditor.DeleteEditorTemplates, name="DeleteEditorTemplates"),
    url(r'^SaveEditorTemplate/$', ckEditor.SaveEditorTemplate, name="SaveEditorTemplate"),
]    