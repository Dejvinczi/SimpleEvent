"""
Core module views.
"""

from rest_framework import (
    mixins,
    viewsets,
)

from .. import models
from . import serializers


class EventViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Event API viewset"""

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
