"""
Core module models.
"""

from django.db import models

class Event(models.Model):
    """Event representation in db."""
    name = models.CharField(max_length=150, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
