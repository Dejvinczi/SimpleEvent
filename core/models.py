"""
Core module models.
"""

from django.db import models

class Event(models.Model):
    """Event representation in db."""
    name = models.CharField(max_length=150, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    
class Artist(models.Model):
    """Artist representation in db."""
    MUSIC_GENRE_CHOICES = [
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('hip_hop', 'Hip Hop'),
        ('country', 'Country'),
    ]
    
    name = models.CharField(unique=True)
    music_genre = models.CharField(max_length=7, choices=MUSIC_GENRE_CHOICES)