from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Django settings.py faylini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)

# Celery uchun broker urinishlarini boshqarish
app.conf.broker_connection_retry = True
app.conf.broker_connection_retry_on_startup = True

# Django settings'dan Celery sozlamalarini yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django-dagi barcha app'lardan task'larni avtomatik kiritish
app.autodiscover_tasks()
