"""Development settings and globals."""
from .base import *
from django.utils.crypto import get_random_string
from os.path import  basename, dirname, join, abspath
import os,dj_database_url
from decouple import config, Csv
########## DEBUG CONFIGURATION
DEBUG = config('DEBUG', default=False , cast=bool)
########## END DEBUG CONFIGURATION
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# CSRF_COOKIE_DOMAIN = '.localhost.com'

########## EMAIL CONFIGURATION
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT',default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default="")
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default="")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER',default="")
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = config('TWILIO_FROM_NUMBER')


########## END EMAIL CONFIGURATION
########## MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

########## DATABASE CONFIGURATION
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

CONN_MAX_AGE = 600  
DATABASES = {
    'default': dj_database_url.config(
          default=config('DATABASE_URL')
      )
 }


# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'OPTIONS': {
            'server_max_value_length': 1024 * 1024 * 2,
        }
    }
}
########## END CACHE CONFIGURATION


########## DJANGO-DEBUG-TOOLBAR CONFIGURATION
# MIDDLEWARE_CLASSES += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

BUILTIN_APPS += [
    'debug_toolbar',
    'debug_panel',
    # 'template_debug'
]

INSTALLED_APPS = BUILTIN_APPS + USER_APPS
# TEMPLATE_DEBUG = True


# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('127.0.0.1',)
ENABLE_STACKTRACES = True
MIDDLEWARE_CLASSES = [

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'appointmentscheduler.middleware.LoginRequiredMiddleware',
    'appointmentscheduler.middleware.VisitorDetails',

]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

def custom_show_toolbar(request):
    return False
DEBUG_TOOLBAR_CONFIG = {
    # If set to True (default), the debug toolbar will show an intermediate
    # page upon redirect so you can view any debug information prior to
    # redirecting. This page will provide a link to the redirect destination
    # you can follow when ready. If set to False, redirects will proceed as
    # normal.
    'INTERCEPT_REDIRECTS': False,

    # If not set or set to None, the debug_toolbar middleware will use its
    # built-in show_toolbar method for determining whether the toolbar should
    # show or not. The default checks are that DEBUG must be set to True and
    # the IP of the request must be in INTERNAL_IPS. You can provide your own
    # method for displaying the toolbar which contains your custom logic. This
    # method should return True or False.
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,

    # An array of custom signals that might be in your project, defined as the
    # python path to the signal.
    'EXTRA_SIGNALS': [],

    # If set to True (the default) then code in Django itself won't be shown in
    # SQL stacktraces.
    'HIDE_DJANGO_SQL': False,

    # If set to True (the default) then a template's context will be included
    # with it in the Template debug panel. Turning this off is useful when you
    # have large template contexts, or you have template contexts with lazy
    # datastructures that you don't want to be evaluated.
    'SHOW_TEMPLATE_CONTEXT': True,

    # If set, this will be the tag to which debug_toolbar will attach the debug
    # toolbar. Defaults to 'body'.
    'TAG': 'body',
}
########## END DJANGO-DEBUG-TOOLBAR CONFIGURATION


########## CELERY CONFIGURATION

########## END CELERY CONFIGURATIONs


########## LOGGING CONFIGURATION
LOG_DIR = join( BASE_DIR, 'log')

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
########## LOGGING CONFIGURATION
DJANGO_LOG_LEVEL=DEBUG 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)-7s %(thread)-5d %(message)s',
            'datefmt': '%H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(funcName)s|%(lineno)s|%(process)d|%(thread)d|%(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s|%(message)s'
        },
    
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        
        'console': {  # Log to stdout
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'short'
        },
        
        'default': {
            'level':'DEBUG',
            'filters': ['require_debug_true'],
            'class':'logging.handlers.RotatingFileHandler',
            'filename': join(LOG_DIR, 'app.log'),
            'maxBytes': 1024*1024*10, # 5 MB
            'backupCount': 0,
            'formatter':'simple',

        },

        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  join(LOG_DIR, 'celery.log'),
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        },
        'logfile': {  # Rotate log file daily, only keep 1 backup
            'level':'DEBUG',
            'filters': ['require_debug_true'],
            'class':'logging.handlers.RotatingFileHandler',
            'filename': join(LOG_DIR, 'django.log'),
            'maxBytes': 1024*1024*10, # 5MB
            'backupCount': 0,
            'formatter': 'verbose',
        },
        'null': {
            'level':'DEBUG',
            'class': 'logging.NullHandler',
        },

    },
    # EMAIL all errors (might not want this, but let's try it)
    'root': {  # For dev, show errors + some info in the console
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
       'django.template': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['logfile'],
        },
       
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },   
        'django.security.DisallowedHost': {
            'handlers': [],
            'propagate': False,
        },
       
    
        'py.warnings': {
            'handlers': ['console'],
        },
        'django.db': {
            'handlers': ['default'],
            'level': 'DEBUG', # Set this to ERROR on production hosts since the database logs are very verbose
            'propagate': False, 
        },
        'celery': {
            'handlers': ['celery'],
            'level': 'DEBUG',
            'propagate': False
        },
        'appointmentscheduler.tasks': {
            'handlers': ['celery'],
            'level': 'DEBUG',
            'propagate': False
        },
       
    },


}
CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_RDB_HOST ='127.0.0.1'
# CELERY_RDB_PORT = 6899
default_port = 6899
CELERY_RDB_HOST = os.environ.get('CELERY_RDB_HOST') or '127.0.0.1'
CELERY_RDB_PORT = int(os.environ.get('CELERY_RDB_PORT') or default_port)
########## END LOGGING CONFIGURATIONs

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}


chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)

# Reminder time: how early text messages are sent in advance of appointments
REMINDER_TIME = 30 # minutes





