"""
Core module API serializers.
"""

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .. import models


class PerformanceSerializer(serializers.ModelSerializer):
    """Performance model serializer."""

    event = serializers.PrimaryKeyRelatedField(
        queryset=models.Event.objects.all(),
        write_only=True,
    )
    artists = serializers.SlugRelatedField(
        queryset=models.Artist.objects.all(),
        many=True,
        slug_field="name",
    )

    class Meta:
        model = models.Performance
        fields = ("id", "event", "artists", "start", "end")

    def validate(self, data: dict):
        # Validations if "start" or "end" in data (getattr is for partial update)
        if any(element in data for element in ["start", "end"]):
            start = data.get("start", getattr(self.instance, "start"))
            end = data.get("end", getattr(self.instance, "end"))

            # Check "end" is not "after" start.
            if start > end:
                message = _("The end may not be earlier than the start")
                raise serializers.ValidationError({"end": message})

            # Check new performance are in event timeframe
            event = data.get("event", getattr(self.instance, "event"))
            if event.start > start or event.end < end:
                message = _("Performance is out of the event timeframe")
                raise serializers.ValidationError({"start": message, "end": message})

            # Check for event performances overlapping other timeframes
            if models.Performance.objects.filter(
                Q(event=event)
                & (Q(start__range=(start, end) | Q(end__range=(start, end))))
            ).exists():
                message = _("Performance timeframe overlaps with anothers")
                raise serializers.ValidationError({"start": message, "end": message})

        return data


class EventSerializer(serializers.ModelSerializer):
    """Event model serializer."""

    class Meta:
        model = models.Event
        fields = ("id", "name", "start", "end")

    def validate(self, data):
        # Validations if "start" or "end" in data (getattr is for partial update)

        if any(element in data for element in ["start", "end"]):
            start = data.get("start", getattr(self.instance, "start"))
            end = data.get("end", getattr(self.instance, "end"))

            # Check "end" is not "after" start.
            if start > end:
                message = _("The end may not be earlier than the start")
                raise serializers.ValidationError({"end": message})

        return data

    def update(self, instance, validated_data):
        # Validations if "start" or "end" in data
        if any(element in validated_data for element in ["start", "end"]):
            start = validated_data.get("start", instance.start)
            end = validated_data.get("end", instance.end)

            # Check event performances is not out of new event timeframe
            if models.Performance.objects.filter(
                Q(event=instance) & (Q(start__lt=start) | Q(end__gt=end))
            ).exists():
                message = _("Some performances are outside of the event timeframe")
                raise serializers.ValidationError({"start": message, "end": message})

        return super().update(instance, validated_data)


class EventRetrieveSerializer(EventSerializer):
    """Event model retrive serializer."""

    performances = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ("performances",)

    @extend_schema_field(PerformanceSerializer(many=True))
    def get_performances(self, instance):
        performances = instance.performances.order_by("start")
        return PerformanceSerializer(performances, many=True).data
