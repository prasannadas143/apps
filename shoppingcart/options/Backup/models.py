from django.db import models

# Create your models here.
class BackupDetails(models.Model):
    backup_time = models.DateTimeField(blank=False, null=False)
    filetype = models.CharField(max_length=100, blank=False, null=False)
    size = models.CharField(max_length=100, blank=False, null=False)
    backupfile = models.FileField(max_length=255)
    
    class Meta:
        # managed = False
        db_table = 'shoppingcart_backups'
        ordering = ['-id']

