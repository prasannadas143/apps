from django.db import models

# Create your models here.

class Options(models.Model):
    # foreign_id = models.IntegerField()
    key = models.CharField(max_length=255)
    tab_id = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    app_name = models.CharField(max_length=255)

    class Meta:
        # managed = False
        db_table = 'options'
