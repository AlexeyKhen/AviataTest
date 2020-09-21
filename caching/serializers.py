from rest_framework import serializers
from .models import *


class FlightSerializer(serializers.ModelSerializer):
    done = serializers.BooleanField(read_only=True)

    class Meta:
        model = Flight
        fields = "__all__"
