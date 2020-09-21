from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from .models import Flight
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .services.cacheCreatorInitial import *
from .tasks import *
from .services.retrievingQueryset import *
from .tasks import creating_and_testing_initial_cache


class FlightListCreateView(ListCreateAPIView):
    queryset = Flight.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FlightSerializer


class FlightsDetailView(RetrieveUpdateAPIView):
    queryset = Flight.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FlightSerializer
    lookup_field = "slug"


def initialize_caching(request):
    creating_and_testing_initial_cache.delay()

    return render(request, 'caching.html')


class AlaTse(ListView):
    template_name = 'directions/ala_tse.html'
    queryset = return_queryset('ALA', 'TSE')


class TseAla(ListView):
    template_name = 'directions/tse_ala.html'
    queryset = return_queryset('TSE', 'ALA')


class AlaMow(ListView):
    template_name = 'directions/ala_mow.html'
    queryset = return_queryset('ALA', 'MOW')


class MowAla(ListView):
    template_name = 'directions/mow_ala.html'
    queryset = return_queryset('MOW', 'ALA')


class AlaCit(ListView):
    template_name = 'directions/ala_cit.html'
    queryset = return_queryset('ALA', 'CIT')


class CitAla(ListView):
    template_name = 'directions/cit_ala.html'
    queryset = return_queryset('CIT', 'ALA')


class TseMow(ListView):
    template_name = 'directions/tse_mow.html'
    queryset = return_queryset('TSE', 'MOW')


class MowTse(ListView):
    template_name = 'directions/mow_tse.html'
    queryset = return_queryset('MOW', 'TSE')


class TseLed(ListView):
    template_name = 'directions/tse_led.html'
    queryset = return_queryset('TSE', 'LED')


class LedTse(ListView):
    template_name = 'directions/led_tse.html'
    queryset = return_queryset('LED', 'TSE')
