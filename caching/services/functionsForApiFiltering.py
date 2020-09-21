import itertools
from pprint import pprint
import requests
from datetime import date
from django.core.cache import cache
from django.utils.text import slugify


def clear_cache():
    cache.clear()


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


def getting_rough_data(fromTo, flyTo, dateFrom, dateTo):
    cache_name = f'first_cache-{fromTo}-{flyTo}-{dateFrom}-{dateTo}'
    if cache_name in cache:
        first_cache = cache.get(cache_name)
    else:
        payload = {"flyFrom": fromTo, "to": flyTo, "dateFrom": dateFrom, "dateTo": dateTo, 'partner': "picky"}
        r = requests.get(
            "https://api.skypicker.com/flights", params=payload)
        first_cache = r.json().get('data')
        cache.set(cache_name, first_cache, timeout=24 * 60 * 60)

    return first_cache


def filtering_data(first_cache, departure, arrival):
    data = {}
    for obj in first_cache:
        timestamp = str((date.fromtimestamp(obj.get('dTime'))))
        key = slugify(f'{timestamp}-{departure}-{arrival}')
        flight_data = {"id_flight": obj.get('id'), 'price': obj.get('price'), 'token': obj.get('booking_token'),

                       "flyFrom": departure, "flyTo": arrival, "date": timestamp}
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


def posting_new_flights_daily_basis(data):
    for key in data.keys():

        if key not in cache:
            obj = data[key][0]
            cache.set(key, obj, timeout=24 * 60 * 60)
            request_put_post('POST', obj, key)


def finding_min_price_and_validation(data):
    i = 0
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
                    print('cont')
                    continue

            if condition:

                if cache.get(key)['id_flight'] == obj['id_flight']:

                    break
                else:
                    request_put_post('PUT', obj, key)
                    cache.set(key, obj, timeout=24 * 60 * 60)

                    i += 1
                break

    print(f'number of changed flights: {i}')
    return None
