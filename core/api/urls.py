"""
Core module API urls.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"events", views.EventViewSet, basename="events")
router.register(r"performances", views.PerformanceViewSet, basename="performances")

app_name = "core"

urlpatterns = [
    path("", include(router.urls)),
]
