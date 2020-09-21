from .functionsForApiFiltering import *
import datetime as dt
from django.core.cache import cache

now = dt.datetime.today()
month_later = now + dt.timedelta(weeks=4)
dateFrom = str(now.strftime('%d/%m/%Y'))
dateTo = str(month_later.strftime('%d/%m/%Y'))

directions = [
    ('ALA', 'TSE'),
    ('TSE', 'ALA'),
    ('ALA', 'MOW'),
    ('MOW', 'ALA'),
    ('ALA', 'CIT'),
    ('CIT', 'ALA'),
    ('TSE', 'MOW'),
    ('MOW', 'TSE'),
    ('TSE', 'LED'),
    ('LED', 'TSE')]


def setting_database(post_type):
    data_to_filter = []
    for direction in directions:
        rough_data = getting_rough_data(direction[0], direction[1], dateFrom, dateTo)
        filtered = filtering_data(rough_data, direction[0], direction[1])
        data_to_filter.append(filtered)
        post_type(filtered)

    for obj in data_to_filter:
        finding_min_price_and_validation(obj)
    cache.set('data_to_filter', data_to_filter, timeout=24 * 60 * 60)


def checking_validation_throught_work():
    data_to_filter = cache.get('data_to_filter')
    for obj in data_to_filter:
        finding_min_price_and_validation(obj)
    cache.set('data_to_filter', data_to_filter, timeout=24 * 60 * 60)
