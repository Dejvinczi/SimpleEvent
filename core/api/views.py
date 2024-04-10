"""
Core module API views.
"""

from django.views.decorators.csrf import csrf_exempt
from rest_framework import (
    mixins,
    viewsets,
    views,
    status,
)
from rest_framework.response import Response
from rest_framework.decorators import action

from ..tasks import generate_csv_and_send_task
from .. import models
from . import serializers


class EventViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
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
            case "initiate_export_csv":
                return serializers.WebhookSerializer
            case _:
                return self.serializer_class

    @action(detail=False, methods=["POST"], url_path="generate-csv")
    def initiate_export_csv(self, request):
        """
        Initiate export events to csv file.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        webhook_url = serializer.validated_data["webhook_url"]

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data

        generate_csv_and_send_task.delay(webhook_url, "event", data)

        return Response(
            {"status": "CSV export process initiated."}, status=status.HTTP_200_OK
        )


class PerformanceViewSet(viewsets.ModelViewSet):
    """Performance API vie wset"""

    queryset = models.Performance.objects.prefetch_related("artists").all()
    serializer_class = serializers.PerformanceSerializer
