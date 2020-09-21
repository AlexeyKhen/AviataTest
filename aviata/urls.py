"""aviata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from caching.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AlaTse.as_view(), name='AlaTse'),
    path('clearcache/', clear_cache_full, name='clear_cache'),
    path('TseAla/', TseAla.as_view(), name='TseAla'),
    path('AlaMow/', AlaMow.as_view(), name='AlaMow'),
    path('MowAla/', MowAla.as_view(), name='MowAla'),
    path('AlaCit/', AlaCit.as_view(), name='AlaCit'),
    path('CitAla/', CitAla.as_view(), name='CitAla'),
    path('TseMow/', TseMow.as_view(), name='TseMow'),
    path('MowTse/', MowTse.as_view(), name='MowTse'),
    path('TseLed/', TseLed.as_view(), name='TseLed'),
    path('LedTse/', LedTse.as_view(), name='LedTse'),
    path('api/', FlightListCreateView.as_view(), name='FlightListCreateView'),
    path('api/<slug>', FlightsDetailView.as_view(), name='FlightsDetailView'),

]
