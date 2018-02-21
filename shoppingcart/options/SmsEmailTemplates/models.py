from django.db import models

# Create your models here.


class SmsEmailTemplates(models.Model):
    TemplateName = models.CharField(max_length=200, blank=False, null=False,unique=True)
    class Meta:
        # managed = False
        db_table = 'templates'
        unique_together = (('TemplateName'),)

class SmsEmailTemplatesDetails(models.Model):
    TemplateID = models.CharField(max_length=200, blank=False, null=False,unique=True)
    subject = models.CharField(max_length=200, blank=False, null=False)
    DesignedTemplate = models.TextField(blank=False, null=False)
    class Meta:
        # managed = False
        db_table = 'templatesDetails'
        unique_together = (('TemplateID'),) 
