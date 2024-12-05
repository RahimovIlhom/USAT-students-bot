from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings.py faylini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Django settings'dan Celery sozlamalarini yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django-dagi barcha app'lardan task'larni avtomatik kiritish
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
