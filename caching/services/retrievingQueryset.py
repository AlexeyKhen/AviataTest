import datetime as dt
from caching.models import Flight

now = dt.datetime.today()
month_later = now + dt.timedelta(weeks=4)


def return_queryset(flyFrom, flyTo):
    data = Flight.objects.filter(flyFrom=flyFrom, flyTo=flyTo) \
        .filter(date__gte=now) \
        .filter(date__lte=month_later) \
        .order_by('date')

    return data
