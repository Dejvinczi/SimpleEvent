"""
Menu module model factories.
"""

import factory
from django.utils import timezone

from .. import models


class EventFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Event{n}")
    start = factory.Faker(
        "date_time_between",
        start_date="-1y",
        end_date="now",
        tzinfo=timezone.get_current_timezone(),
    )
    end = factory.Faker(
        "date_time_between",
        start_date=start,
        end_date="+1y",
        tzinfo=timezone.get_current_timezone(),
    )

    class Meta:
        model = models.Event


MUSIC_GENRE_CHOICES_ELEMENTS = [x[0] for x in models.Artist.MUSIC_GENRE_CHOICES]


class ArtistFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Artist{n}")
    music_genre = factory.Faker("random_element", elements=MUSIC_GENRE_CHOICES_ELEMENTS)

    class Meta:
        model = models.Artist


class PerformanceFactory(factory.django.DjangoModelFactory):
    event = factory.SubFactory(EventFactory)
    start = factory.Faker(
        "date_time_between",
        start_date="-1y",
        end_date="now",
        tzinfo=timezone.get_current_timezone(),
    )
    end = factory.Faker(
        "date_time_between",
        start_date=start,
        end_date="+1y",
        tzinfo=timezone.get_current_timezone(),
    )

    class Meta:
        model = models.Performance
