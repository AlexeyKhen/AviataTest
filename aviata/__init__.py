from __future__ import absolute_import, unicode_literals
from caching.tasks import creating_and_testing_initial_cache
from .celery import app as celery_app

__all__ = ('celery_app',)





