from django.shortcuts import render
from django.shortcuts import  render, HttpResponseRedirect,HttpResponse,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  get_object_or_404
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt,ensure_csrf_cookie
from django import db
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.utils import timezone
from django.core.files import File
from django.core.management import call_command
import pdb,sys, logging, pytz,json
from os.path import basename
from datetime import datetime
from io import StringIO
from datetime import datetime, date, time
import arrow, mimetypes, urllib
from appointmentscheduler.models import  *





# from settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD

@requires_csrf_token
def create_backup(request):
	""" Take  backup of media files and database """
	db_name = db.utils.settings.DATABASES['default']['NAME']
	backup, database, files = None, None, None
	if 'backup' in request.POST and request.POST['backup']:
		backup = request.POST['backup']
	if 'db' in request.POST and request.POST['db']:
		database = request.POST['db']
		# if backup and db :

	if 'files' in request.POST and request.POST['files']:
		files = request.POST['files']
	old = sys.stdout
	out = StringIO()
	sys.stdout = out
	backup_dir = settings.DBBACKUP_STORAGE_OPTIONS['location']
	created_time  = timezone.now()
	if database :
		call_command('dbbackup',stdout=out)
		sys.stdout = sys.__stdout__
		db_details = out.getvalue()
		filetype = "database"
		db_details = 'Backing Up Database: appsdb \nBackup size: 195.8 KiB \nWriting file to : default-DESKTOP-CKOGKNO-2018-01-04-132040.psql \n'
		db_info = db_details.split('\n')
		db_name = db_info[0].split(':')[1].strip()
		db_size = db_info[1].split(':')[1].strip()
		db_file_name = db_info[2].split(':')[1].strip()
		db_file_path = os.path.join(backup_dir, db_file_name )
		bd = BackupDetails(backup_time=created_time,filetype=filetype, size=db_size)
		bd.backupfile.name = db_file_path
		bd.save()
	out.close()
	created_time  = timezone.now()
	media_out = StringIO()
	sys.stdout = media_out
	if files :
		call_command('mediabackup')
		sys.stdout = sys.__stdout__
		media_details = media_out.getvalue()
		media_info = media_details.split('\n')
		media_file_name = media_info[0].split(':')[1].strip()
		filetype = "file"
		media_file_path = os.path.join(backup_dir, media_file_name)
		statinfo = os.stat(media_file_path)
		media_file_size = int(statinfo.st_size/1024)
		media_file_size = str(media_file_size) + " KiB"
		bd = BackupDetails(backup_time=created_time,filetype=filetype, size=media_file_size)
		bd.backupfile.name = media_file_path
		bd.save()
	media_out.close()
	sys.stdout = old
	user_timezone = request.session['visitor_timezone'][0]
	backuplist = []
	backupinstances = BackupDetails.objects.all()
	for backupinstance in  backupinstances:
		backupdetail = dict()
		format = '%Y-%m-%d %H:%M %p'
		backupdetail['created_time'] = backupinstance.backup_time.astimezone(pytz.timezone(user_timezone)).strftime(format)
		backupdetail['filename'] = basename(backupinstance.backupfile.name)
		backupdetail['filesize'] = backupinstance.size
		backupdetail['filetype'] = backupinstance.filetype
		backuplist.append( backupdetail )
	template_name="backup.html"
	templatename=  os.path.join('Options','Backup',template_name)
	return render(request,templatename,{ "backuplist" : backuplist})

def listbackups(request):
	user_timezone = request.session['visitor_timezone'][0]
	backuplist = []
	backupinstances = BackupDetails.objects.all()
	for backupinstance in  backupinstances:
		backupdetail = dict()
		format = '%Y-%m-%d %H:%M %p'
		backupdetail['backupid'] = backupinstance.id
		backupdetail['created_time'] = backupinstance.backup_time.astimezone(pytz.timezone(user_timezone)).strftime(format)
		backupdetail['filename'] = basename(backupinstance.backupfile.name)
		backupdetail['filesize'] = backupinstance.size
		backupdetail['filetype'] = backupinstance.filetype
		backuplist.append( backupdetail )
	return  HttpResponse(json.dumps({"data" :backuplist }), content_type='application/json')   

@requires_csrf_token
def deletebackup(request,id=None):
    """ Delete booking """

    backupinstance = get_object_or_404( BackupDetails,  pk=int(id) )
    backupinstance.delete()
    return  HttpResponse(status=204) 

@requires_csrf_token
def deletebackups(request):
    """ Delete list of booking """

    deleteids= request.POST['rowids']
    for id in deleteids.split(",") :
        backupinstance=get_object_or_404( BackupDetails,  pk=int(id) )
        backupinstance.delete()

    return  HttpResponse(status=204)  

@requires_csrf_token
def downloadbackup(request,id=None):
    """ Download backup file """
    backupinstance = get_object_or_404( BackupDetails,  pk=int(id) )
    chunk_size = 8192
    downloadfile = basename(backupinstance.backupfile.name)
    download_filepath = backupinstance.backupfile.path
    response = StreamingHttpResponse(FileWrapper(open(download_filepath, 'rb'), chunk_size))

    filetype, encoding = mimetypes.guess_type(download_filepath)
    if filetype is None:
        filetype = 'application/octet-stream'
    response['Content-Type'] = filetype
    response['Content-Length'] = os.stat(download_filepath).st_size
    if encoding is not None:
        response['Content-Encoding'] = encoding
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(downloadfile)
    return response
