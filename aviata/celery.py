from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aviata.settings')

app = Celery('aviata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# crontab('*/2 * * * *')
app.conf.beat_schedule = {
    'every-30-minutes': {
        'task': 'caching.tasks.updatingCacheEvery30',
        'schedule': crontab(minute='*/50'),

    },
    'every-midnight': {
        'task': 'caching.tasks.posting_new_cache_daily',
        'schedule': crontab(minute=0, hour=0),

    }}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
