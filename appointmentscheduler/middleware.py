from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseRedirect, Http404  
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from easy_timezones.utils import get_ip_address_from_request, is_valid_ip, is_local_ip
from pytz import country_timezones
from os.path import  basename, dirname, join
from re import compile
import datetime,re,pytz,calendar,json
from appsplatform.settings.base import BASE_DIR




class VisitorDetails(object):

    # Check if client IP is allowed
    def process_request(self, request):
        ip = get_ip_address_from_request(request)
        request.session['visitor_ip'] = ip
        user_timezone = getusertimezone(ip)
        request.session['visitor_timezone'] = user_timezone


def get_ip_address_from_request(request):
    """ Makes the best attempt to get the client's real IP or return the loopback """
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    return ip_address

def getusertimezone(ip):
    g = GeoIP2()
    geoinfo = g.city('74.125.79.147')
    return country_timezones[geoinfo['country_code']]




EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr.lstrip('/')) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middleware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                login_url = settings.LOGIN_URL + "?next=" + request.path
                return HttpResponseRedirect(login_url)
        else :
            appsconfigfile =  join(BASE_DIR, "appsplatform", "config", "user_apps.json") 
            with open(appsconfigfile, 'r') as f:
                datastore = json.load(f)
            user = get_object_or_404(User,id=request.user.id)
            user_group_details = user.groups.values()
            assigned_apps = []
            assigned_app_urls = dict()
            if user_group_details.exists():
                assigned_apps = list(user_group_details)
            for assigned_app in assigned_apps:
                if assigned_app['name'] in datastore :
                    assigned_app_urls[assigned_app['name']] = datastore[assigned_app['name']]
            requested_url = request.path
            request_app = requested_url.split("/")[1]
            print(request_app)
            flag = 0
            for appname,appurl in assigned_app_urls.items() :
                appstring = appurl.split("/")[1]
                print(appstring)
                if request_app == appstring :
                    flag = 1
            exempt_apps = ["accounts" , "home" ]
            if request.user.is_superuser :
                exempt_apps.append("admin")
            if request_app in exempt_apps:
                flag = 1

            if not flag :
                raise Http404  
