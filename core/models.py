"""
Core module models.
"""

from django.db import models


class Event(models.Model):
    """Event representation in db."""

    name = models.CharField(max_length=150, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name


class Artist(models.Model):
    """Artist representation in db."""

    MUSIC_GENRE_CHOICES = [
        ("rock", "Rock"),
        ("pop", "Pop"),
        ("hip_hop", "Hip Hop"),
        ("country", "Country"),
    ]

    name = models.CharField(unique=True)
    music_genre = models.CharField(max_length=7, choices=MUSIC_GENRE_CHOICES)

    def __str__(self):
        return self.name


class Performance(models.Model):
    """Performance representation in db."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    artists = models.ManyToManyField(Artist, related_name="performances")
    start = models.DateTimeField()
    end = models.DateTimeField()
