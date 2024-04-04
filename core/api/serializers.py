"""
Core module serializers.
"""

from rest_framework import serializers
from .. import models


class EventSerializer(serializers.ModelSerializer):
    """Event model serializer."""

    class Meta:
        model = models.Event
        fields = "__all__"
