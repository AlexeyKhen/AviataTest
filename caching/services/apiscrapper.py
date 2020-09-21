import itertools
from pprint import pprint
import requests
from datetime import date
from django.core.cache import cache
from django.utils.text import slugify


def request_put_post(type_of, obj, key):
    data = {'date': obj.get('date'),
            'flyFrom': obj.get('flyFrom'),
            'flyTo': obj.get('flyTo'),
            'id_flight': obj.get('id_flight'),
            'token': obj.get('token'),
            'price': obj.get('price'),
            'slug': key}
    if type_of == "PUT":
        requests.put(f'http://localhost:8000/api/{key}', data=data)

    if type_of == "POST":
        requests.post('http://localhost:8000/api/', data=data)


def getting_rough_data():
    if 'first_cache' in cache:
        first_cache = cache.get('first_cache')
    else:

        payload = {"flyFrom": "TSE", "to": "ALA", "dateFrom": "8/11/2020", "dateTo": "18/12/2020", 'partner': "picky"}
        r = requests.get(
            "https://api.skypicker.com/flights", params=payload)
        first_cache = r.json().get('data')

        cache.set('first_cache', first_cache, timeout=24 * 60 * 60)
    return first_cache


def filtering_data(first_cache):
    data = {}
    for obj in first_cache:
        timestamp = str((date.fromtimestamp(obj.get('dTime'))))
        flyFrom = obj.get('flyFrom')
        flyTo = obj.get('flyTo')
        key = slugify(f'{timestamp}-{flyFrom}-{flyTo}')
        flight_data = {"id_flight": obj.get('id'), 'price': obj.get('price'), 'token': obj.get('booking_token'),

                       "flyFrom": flyFrom, "flyTo": flyTo, "date": timestamp}
        if key not in data.keys():
            data[key] = [flight_data]
        else:
            data[key].append(flight_data)

    return data


def posting_flights(data):
    for key in data.keys():
        if key in cache:
            obj = cache.get(key)
            request_put_post('PUT', obj, key)

        else:
            obj = data[key][0]
            cache.set(key, obj, timeout=24 * 60 * 60)
            request_put_post('POST', obj, key)


def updating_data(old_data, new_data):
    i = 0
    for key in new_data.keys():
        i += 1
        if not (old_data[key] == new_data[key]):
            obj = new_data[key]
            request_put_post('PUT', obj, key)
    print(i)


def finding_min_price_and_validation(data):
    if 'filtered' in cache:
        new_array = cache.get('filtered')
    else:
        new_array = {}
        for key in data.keys():
            list_cycle = itertools.cycle(data[key])
            for obj in data[key]:
                token = obj.get("token")

                payload = {"v": 2, "booking_token": token, 'bnum': 1, 'pnum': 1}
                r = requests.get("https://booking-api.skypicker.com/api/v0.1/check_flights", params=payload)
                flight_data = r.json()

                condition = not flight_data.get("flights_invalid") and flight_data.get("flights_checked")

                if flight_data.get('price_change'):
                    obj['price'] = flight_data.get('total')
                    if obj['price'] > next(list_cycle)['price']:
                        continue

                if condition:
                    new_array[key] = obj
                    break

        cache.set('filtered', new_array, timeout=24 * 60 * 60)

    return new_array
