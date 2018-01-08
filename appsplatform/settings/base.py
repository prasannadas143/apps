"""
Django settings for appsplatform project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os,sys
from decouple import Config, RepositoryEnv
from os.path import  basename, dirname, join
from django.contrib.messages import constants as messages
from django.utils.crypto import get_random_string


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(dirname(os.path.abspath(__file__))))
# Site name.
SITE_NAME = basename(BASE_DIR)

# Absolute filesystem path to the top-level project folder.
SITE_ROOT = dirname(BASE_DIR)

# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DOTENV_FILE =  join(SITE_ROOT, "deploy", ".env") 
config = Config(RepositoryEnv(DOTENV_FILE))

# SECURITY WARNING: keep the secret key used in production secret!
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)
########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(SITE_ROOT)
sys.path.append(SITE_NAME)
sys.path.append(BASE_DIR)

    
########## END PATH CONFIGURATION


# SECURITY WARNING: don't run with debug turned on in production!
########## DEBUG CONFIGURATION
# Disable debugging by default.
DEBUG = False
########## END DEBUG CONFIGURATION

########## KEY CONFIGURATION
# Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.


########## END KEY CONFIGURATION


BUILTIN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'timezone_field',
    'phonenumber_field',
    'djng',
    'bootstrap3',
    'registration',
    'django_celery_results',
    'dbbackup',
    
]

USER_APPS = [
    'appointmentscheduler',
    'appointmentscheduler.templatetags',
]

INSTALLED_APPS = BUILTIN_APPS + USER_APPS
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': join(MEDIA_ROOT,"backup")  }

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'appointmentscheduler.middleware.VisitorDetails',

]

INCLUDE_REGISTER_URL = True
INCLUDE_AUTH_URLS = True
X_FRAME_OPTIONS = 'DENY'
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.





ROOT_URLCONF = 'appsplatform.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
                os.path.join(BASE_DIR,"appointmentscheduler", 'templates'),
                os.path.join(BASE_DIR, "appointmentscheduler", 'templates',"Options"),
                os.path.join(BASE_DIR, "appointmentscheduler", 'templates',"Options","Booking") ,
                os.path.join(BASE_DIR, 'registration', 'templates'),
                os.path.join(BASE_DIR, 'registration', 'auth','templates'),
            ],

    'APP_DIRS': True,  
    'OPTIONS': {
        
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
      
    },

    
}]



WSGI_APPLICATION = 'appsplatform.wsgi.application'


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

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'), 
        'DISABLE_SERVER_SIDE_CURSORS': True,

    },

    
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

########## EMAIL CONFIGURATION



########## END EMAIL CONFIGURATION

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "assets")
STATICFILES_DIRS = (
os.path.join(BASE_DIR, "static"),
)
GEOIP_PATH = join(BASE_DIR,  'geopath')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATIC_URL = '/static/'
####### End  Static files Config

########## Message  CONFIGURATION

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

########## END Message CONFIGURATION


# Application definition
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_DEFAULT_QUEUE = 'normal'
CELERY_DEFAULT_EXCHANGE = 'normal'
CELERY_DEFAULT_ROUTING_KEY = 'normal'
CELERY_REDIRECT_STDOUTS = True
# CELERY_RESULT_BACKEND = 'django-db'


CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'
CELERY_ALWAYS_EAGER = False

# Address of Redis instance, our Celery broker


########## Security CONFIGURATION

# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

########## End CONFIGURATION

# import djcelery
# djcelery.setup_loader()
# BROKER_URL="django:// "

########## URL CONFIGURATION
    # ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

########## Session CONFIGURATION

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_AGE = 60
########## End CONFIGURATION

