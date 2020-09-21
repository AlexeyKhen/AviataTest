from celery import shared_task
from .services.cacheCreatorInitial import *
from .services.functionsForApiFiltering import posting_flights, posting_new_flights_daily_basis


@shared_task
def creating_and_testing_initial_cache():
    setting_database(posting_flights)
    return None


@shared_task
def updatingCacheEvery30():
    checking_validation_throught_work()
    return None


@shared_task
def posting_new_cache_daily():
    setting_database(posting_new_flights_daily_basis)
    return None
