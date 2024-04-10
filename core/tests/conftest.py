"""
Configuration our tests user module tests.
"""

import pytest
from rest_framework.test import APIClient

from ..models import (
    Event,
    Artist,
    Performance,
)
from .factories import (
    EventFactory,
    ArtistFactory,
    PerformanceFactory,
)


@pytest.fixture
def event_model():
    """Fixture to provide Event model"""
    return Event


@pytest.fixture
def event_factory():
    """Fixture to provide MenuFactory."""
    return EventFactory


@pytest.fixture
def artist_model():
    """Fixture to provide Artist model"""
    return Artist


@pytest.fixture
def artist_factory():
    """Fixture to provide ArtistFactory."""
    return ArtistFactory


@pytest.fixture
def performance_model():
    """Fixture to provide Performance model"""
    return Performance


@pytest.fixture
def performance_factory():
    """Fixture to provide PerformanceFactory."""
    return PerformanceFactory


@pytest.fixture
def api_client():
    return APIClient()
