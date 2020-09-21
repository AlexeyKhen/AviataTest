from celery import shared_task
from .services.cacheCreator import *


@shared_task
def creating_and_testing_initial_cache():
    setting_database()
    return None
