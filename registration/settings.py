from appsplatform.settings.base import BASE_DIR, TEMPLATES
from os.path import   join


INCLUDE_REGISTER_URL = True
INCLUDE_AUTH_URLS = True
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.
LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

LOGIN_EXEMPT_URLS = (
'/admin/',
'/accounts/login/',
'/accounts/password/reset/',
'/accounts/password/reset/complete/',
'/accounts/password/reset/done/',
'/accounts/register/',
'/accounts/register/closed/',
'/accounts/activate/complete/'
'/accounts/activate/resend/',
'/accounts/register/complete/',
'/accounts/register/closed/',

 # allow any URL under /legal/*
) 

TEMPLATES[0]['DIRS'] += [  
	join(BASE_DIR, 'registration', 'templates'),
	join(BASE_DIR, 'registration', 'auth','templates') 
]

