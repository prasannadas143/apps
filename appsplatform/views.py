from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import  render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.conf import settings
from os.path import  basename, dirname, join
import json
import pdb
UserModel = get_user_model()



def home(request):
    appsconfigfile =  join(settings.BASE_DIR, "appsplatform", "config", "user_apps.json") 
    with open(appsconfigfile, 'r') as f:
        datastore = json.load(f)
    if request.user.is_authenticated :
        user = get_object_or_404(User,id=request.user.id)
        user_group_details = user.groups.values()
        assigned_apps = []
        assigned_app_urls = dict()
        if user_group_details.exists():
            assigned_apps = list(user_group_details)
        for assigned_app in assigned_apps:
            if assigned_app['name'] in datastore :
                assigned_app_urls[assigned_app['name']] = datastore[assigned_app['name']]
        if  request.user.is_staff :
            return render(request, "user_registration/staff_profile.html",{"userobj" : user \
            ,"assigned_apps" : assigned_app_urls }) 
        elif  request.user.is_active :
            return render(request, "user_registration/customer_profile.html",{"userobj" : user \
            ,"assigned_apps" : assigned_app_urls })   


    else :
        return HttpResponseRedirect( reverse('auth_login') )
