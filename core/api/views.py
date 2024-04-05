"""
Core module API views.
"""

from rest_framework import (
    mixins,
    viewsets,
)

from .. import models
from . import serializers


class EventViewSet(viewsets.ModelViewSet):
    """Event create, update, retrive API viewset"""

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        match self.action:
            case "retrieve":
                return models.Event.objects.prefetch_related(
                    "performances", "performances__artists"
                ).all()
            case _:
                return self.queryset

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return serializers.EventRetrieveSerializer
            case _:
                return self.serializer_class


class PerformanceViewSet(viewsets.ModelViewSet):
    """Performance API viewset"""

    queryset = models.Performance.objects.prefetch_related("artists").all()
    serializer_class = serializers.PerformanceSerializer
