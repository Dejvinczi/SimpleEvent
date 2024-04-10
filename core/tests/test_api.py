"""Core module API tests."""

import pytest
from django.utils import timezone
from django.urls import reverse

from core.api import serializers

EVENT_URL = reverse("core:events-list")
EVENT_INITIATE_EXPORT_CSV_URL = reverse("core:events-initiate-export-csv")

PERFORMANCE_URL = reverse("core:performances-list")


def get_event_detail_url(event):
    """Get event detail url."""
    return reverse("core:events-detail", args=[event.id])


def get_performance_detail_url(performance):
    """Get performance detail url."""
    return reverse("core:performances-detail", args=[performance.id])


@pytest.mark.django_db
class TestPublicEventAPI:
    """Public Event API tests."""

    def test_create_event(self, api_client):
        """Test create event."""
        payload = {
            "name": "TestEvent",
            "start": "2024-01-01 00:00:00",
            "end": "2024-01-02 00:00:00",
        }

        response = api_client.post(EVENT_URL, payload)

        assert response.status_code == 201
        assert response.data["name"] == payload["name"]
        assert response.data["start"] == payload["start"]
        assert response.data["end"] == payload["end"]

    def test_update_event(self, api_client, event_factory):
        """Test update event."""
        event = event_factory.create()
        event_detail_url = get_event_detail_url(event)
        payload = {"name": "TestEventNew"}

        response = api_client.patch(event_detail_url, payload)
        event.refresh_from_db()

        assert response.status_code == 200
        assert event.name == payload["name"]

    def test_update_event_out_of_timeframe(
        self, api_client, event_factory, performance_factory
    ):
        """Test update event out of timeframe."""
        event = event_factory.create(
            start=timezone.make_aware(timezone.datetime(2024, 1, 1, 10, 0, 0)),
            end=timezone.make_aware(timezone.datetime(2024, 1, 1, 12, 0, 0)),
        )
        _ = performance_factory.create(
            event=event,
            start=timezone.make_aware(timezone.datetime(2024, 1, 1, 11, 0, 0)),
            end=timezone.make_aware(timezone.datetime(2024, 1, 1, 12, 0, 0)),
        )

        event_detail_url = get_event_detail_url(event)
        payload = {"end": "2024-01-01 11:00:00"}
        response = api_client.patch(event_detail_url, payload)

        assert response.status_code == 400

    def test_retrieve_event(self, api_client, event_factory):
        """Test retrieve event."""
        event = event_factory.create()
        event_detail_url = get_event_detail_url(event)

        response = api_client.get(event_detail_url)
        serializer = serializers.EventRetrieveSerializer(instance=event)

        assert response.status_code == 200
        assert response.data == serializer.data

    def test_initiate_export_csv(self, api_client):
        """Test initiate export csv."""
        payload = {"webhook_url": "http://test.com/test"}
        response = api_client.post(EVENT_INITIATE_EXPORT_CSV_URL, payload)

        assert response.status_code == 200


@pytest.mark.django_db
class TestPublicPerformanceAPI:
    """Public Performance API tests."""

    def test_create_performance(self, api_client, event_factory):
        """Test create performance."""
        event = event_factory.create(
            start=timezone.make_aware(timezone.datetime(2024, 1, 1, 10, 0, 0)),
            end=timezone.make_aware(timezone.datetime(2024, 1, 1, 12, 0, 0)),
        )
        performance_data = {
            "event": event.id,
            "start": "2024-01-01 10:00:00",
            "end": "2024-01-01 11:00:00",
        }

        response = api_client.post(PERFORMANCE_URL, performance_data)

        assert response.status_code == 201
        assert response.data["start"] == performance_data["start"]
        assert response.data["end"] == performance_data["end"]

    def test_update_performance(self, api_client, event_factory, performance_factory):
        """Test update performance."""
        event = event_factory.create(
            start=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 10, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
            end=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 12, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
        )
        performance = performance_factory.create(
            event=event,
            start=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 10, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
            end=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 11, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
        )

        performance_detail_url = get_performance_detail_url(performance)
        payload = {
            "end": "2024-01-01 12:00:00",
        }

        response = api_client.patch(performance_detail_url, payload)
        assert response.status_code == 200
        assert response.data["end"] == payload["end"]

    def test_update_performance_out_of_event_timeframe(
        self, api_client, event_factory, performance_factory
    ):
        """Test update performance out of timeframe."""
        event = event_factory.create(
            start=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 10, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
            end=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 12, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
        )
        performance = performance_factory.create(
            event=event,
            start=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 10, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
            end=timezone.make_aware(
                timezone.datetime(2024, 1, 1, 11, 0, 0),
                timezone=timezone.get_current_timezone(),
            ),
        )

        performance_detail_url = get_performance_detail_url(performance)
        payload = {
            "end": "2024-01-01 13:00:00",
        }

        response = api_client.patch(performance_detail_url, payload)

        assert response.status_code == 400

    def test_delete_performance(
        self, api_client, event_factory, performance_model, performance_factory
    ):
        """Test delete performance."""
        event = event_factory.create()
        performance = performance_factory.create(event=event)

        performance_detail_url = get_performance_detail_url(performance)
        response = api_client.delete(performance_detail_url)

        assert response.status_code == 204
        assert not performance_model.objects.filter(id=performance.id).exists()
