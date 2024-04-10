"""Core module models tests."""

import pytest
from django.utils import timezone


@pytest.mark.django_db
class TestEventModel:
    """Test Event model."""

    def test_create_event(self, event_model):
        """Test create event method."""
        event_data = {
            "name": "TestEvent",
            "start": timezone.make_aware(timezone.datetime(2024, 1, 1)),
            "end": timezone.make_aware(timezone.datetime(2024, 1, 2)),
        }

        event = event_model.objects.create(**event_data)

        assert str(event) == event_data["name"]


@pytest.mark.django_db
class TestArtistModel:
    """Test Artist model."""

    def test_create_artist(self, artist_model):
        """Test create artist method."""
        artist_data = {
            "name": "TestArist",
            "music_genre": "rock",
        }

        artist = artist_model.objects.create(**artist_data)

        assert str(artist) == artist_data["name"]


@pytest.mark.django_db
class TestPerformanceModel:
    """Test Performance model."""

    def test_create_performance(self, event_factory, artist_factory, performance_model):
        """Test create performance method."""
        event = event_factory.create()
        performance_data = {
            "event": event,
            "start": timezone.make_aware(timezone.datetime(2024, 1, 1)),
            "end": timezone.make_aware(timezone.datetime(2024, 1, 2)),
        }

        performance = performance_model.objects.create(**performance_data)
        artists = artist_factory.create_batch(3)
        performance.artists.set(artists)
        performance.save()

        assert performance.event == performance_data["event"]
        assert performance.start == performance_data["start"]
        assert performance.end == performance_data["end"]
        assert performance.artists.count() == 3

        for performance_artist in performance.artists.all():
            assert performance_artist in artists
