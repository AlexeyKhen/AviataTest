from .apiscrapper import *
import datetime as dt

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


def setting_database():
    for direction in directions:
        rough_data = getting_rough_data(direction[0], direction[1], dateFrom, dateTo)
        filtered = filtering_data(rough_data, direction[0], direction[1])
        posting_flights(filtered)
