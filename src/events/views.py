from rest_framework import generics
from django.shortcuts import render

from src.events.models import Event
from .serializer import EventSerializer


# Create your views here.
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
