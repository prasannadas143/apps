"""
Views which allow users to create and activate accounts.

"""
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import ParentChildUser
from registration.forms import ResendActivationForm, CustomUserCreationForm
from django.contrib.auth.models import User
from registration.models import ParentChildUser
from django.contrib.auth.models import Group, PermissionsMixin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

import pdb
UserModel = get_user_model()

REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM',
                                 'registration.forms.RegistrationForm')
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = getattr(
    settings, 'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS', True)

UserModel = get_user_model()

class RegistrationView(FormView):
    """
    Base class for user registration views.

    """
    disallowed_url = 'registration_disallowed'
    form_class = REGISTRATION_FORM
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'user_registration/registration_form.html'

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed and if user is logged in before even bothering to
        dispatch or do other processing.

        """
        if ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS:
            if self.request.user.is_authenticated:
                if settings.LOGIN_REDIRECT_URL is not None:
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    raise Exception((
                        'You must set a URL with LOGIN_REDIRECT_URL in '
                        'settings.py or set '
                        'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS=False'))

        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, form):
        """
        Implement user-registration logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user=None):
        """
        Use the new user when constructing success_url.

        """
        return super(RegistrationView, self).get_success_url()


class ActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    http_method_names = ['get']
    template_name = 'user_registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


class ResendActivationView(FormView):
    """
    Base class for resending activation views.
    """
    form_class = ResendActivationForm
    template_name = 'user_registration/resend_activation_form.html'

    def form_valid(self, form):
        """
        Regardless if resend_activation is successful, display the same
        confirmation template.

        """
        self.resend_activation(form)
        return self.render_form_submitted_template(form)

    def resend_activation(self, form):
        """
        Implement resend activation key logic here.
        """
        raise NotImplementedError

    def render_form_submitted_template(self, form):
        """
        Implement rendering of confirmation template here.

        """
        raise NotImplementedError


class ApprovalView(TemplateView):

    http_method_names = ['get']
    template_name = 'user_registration/admin_approve.html'

    def get(self, request, *args, **kwargs):
        approved_user = self.approve(*args, **kwargs)
        if approved_user:
            success_url = self.get_success_url(approved_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ApprovalView, self).get(request, *args, **kwargs)

    def approve(self, *args, **kwargs):
        """
        Implement admin-approval logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError



def createUser(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():

            userobj = f.save()
            pcu = ParentChildUser(parentuser = request.user.id,
                                    childuser =  userobj.pk)
            us = User.objects.get(id=userobj.pk)
            pcu.user = us
            pcu.save()
            messages.success(request, 'Account created successfully')
            return redirect(reverse('user_home')) 
    else:
        f = CustomUserCreationForm()

    return render(request, 'user_registration/add_user.html', {'form': f})

def manageaccount(request):
    if request.user.is_authenticated  and request.user.is_staff:
        parentid = request.user.id
        childids = ParentChildUser.objects.filter( parentuser = parentid )
        customers = []
        if childids.exists():
            for childid in childids :
                childobj = UserModel.objects.get( id = childid.childuser )
                customers.append( childobj )
    return render(request, "user_registration/userlist.html",{ "customers" : customers })   
        


def userdetails(request,userid):
    if request.user.is_authenticated  and request.user.is_staff:
        buisness_user_id = request.user.id
        buisness_user = get_object_or_404(UserModel, id=buisness_user_id)
        buisness_user_group_details = buisness_user.groups.values()
        available_apps, added_apps = [],[]
        if buisness_user_group_details.exists():
            available_apps = list(buisness_user_group_details)
        user = get_object_or_404(UserModel, id=userid)
        user_group_details = user.groups.values()
        assigned_apps = []
        if user_group_details.exists():
            assigned_apps = list(user_group_details)
        appids = [ appdata["id"] for appdata in assigned_apps ] 
        ind=0
        while ind < len( available_apps ):
            if available_apps[ind]["id"] in appids:
                del available_apps[ind]
                ind -= 1
            ind+=1
    return render(request, "user_registration/userdetails.html",{"userobj" : user,\
         "available_apps" : available_apps ,"assigned_apps" : assigned_apps })  

def saveuserapp(request):
    username = request.POST["username"]
    user_email = request.POST["useremail"]
    apps_available = request.POST["apps_available"]
    #Get user id
    userobj = get_object_or_404(UserModel, username=username)
    userid = userobj.id
    app_elements  = apps_available.split(":")
    groupsid = [ elm['id']  for elm in userobj.groups.values('id') ]
    
    if request.user.is_authenticated  and request.user.is_staff:

        for app_element in app_elements:
            if app_element :

                if int(app_element) in groupsid:
                    continue
                elif app_element  : 
                    group = get_object_or_404(Group, id=int(app_element))
                    userobj.groups.add(group)
                    appname = group.name
                    messages.success(request, "App " + appname + ' added successfully to user')
        for groupid in groupsid:
            if str(groupid) not in app_elements:
                gp = Group.objects.get(id= int(groupid))
                appname = gp.name
                userobj.groups.remove(gp)
                messages.warning(request,"App " + appname + " is removed from the user")
    return HttpResponseRedirect( reverse('customerdetails',  args=[userid]) )
