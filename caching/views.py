from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from caching.services.apiscrapper import *


class FlightListCreateView(ListCreateAPIView):
    queryset = Flight.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FlightSerializer


class FlightsDetailView(RetrieveUpdateAPIView):
    queryset = Flight.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FlightSerializer
    lookup_field = "slug"


def home(request):
    cacheFirst = getting_rough_data()
    data = filtering_data(cacheFirst)
    posting_flights(data)
    newdata = finding_min_price_and_validation(data)
    updating_data(data, newdata)
    return render(request, "home.html")
