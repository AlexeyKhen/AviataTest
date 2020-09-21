from __future__ import absolute_import, unicode_literals
from caching.tasks import  creating_and_testing_initial_cache

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

creating_and_testing_initial_cache.delay()

