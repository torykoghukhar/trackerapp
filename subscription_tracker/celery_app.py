import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackerapp.settings')

app = Celery('trackerapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
