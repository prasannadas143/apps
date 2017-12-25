"""Development settings and globals."""


from .base import *
from django.utils.crypto import get_random_string


########## DEBUG CONFIGURATION
DEBUG = True
########## END DEBUG CONFIGURATION
ALLOWED_HOSTS = [ '127.0.0.1', 'localhost',]


########## EMAIL CONFIGURATION
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'daspython@gmail.com'
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'daspython@gmail.com'


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

USER_APPS += [
    'debug_toolbar',
    'debug_panel',

]

INSTALLED_APPS = BUILTIN_APPS + USER_APPS



# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('127.0.0.1',)
ENABLE_STACKTRACES = True

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
LOG_DIR = os.path.join( BASE_DIR, 'log')

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
########## LOGGING CONFIGURATION

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
        'null': {
            'level':'DEBUG',
            'class': 'logging.NullHandler',
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
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'maxBytes': 1024*1024*10, # 5 MB
            'backupCount': 0,
            'formatter':'simple',

        },
        'logfile': {  # Rotate log file daily, only keep 1 backup
            'level':'DEBUG',
            'filters': ['require_debug_true'],
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': 1024*1024*10, # 5MB
            'backupCount': 0,
            'formatter': 'verbose',
        },

        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'celery.log',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
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
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True
        },
       
    },


}

########## END LOGGING CONFIGURATIONs

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)

# Reminder time: how early text messages are sent in advance of appointments
REMINDER_TIME = 30 # minutes





