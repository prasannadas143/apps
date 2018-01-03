from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appsplatform.settings.local')

from django.conf import settings

app = Celery('Appsplatform', broker='amqp://localhost//',
			     backend='amqp://')

app.config_from_object('django.conf:settings')
app.conf.update(
	result_backend='django-db',
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json', )
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
