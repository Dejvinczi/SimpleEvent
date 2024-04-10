"""Core module helpers tests."""

import os
import csv
import pytest

from django.utils import timezone
from django.conf import settings

from core.helpers import (
    generate_csv_from_queryset,
    generate_csv_from_serialized_data,
)


@pytest.mark.django_db
class TestCSVGeneration:
    """Test CSV generation functions."""

    def test_generate_csv_from_queryset_without_media_root_folder(self, event_model):
        if os.path.exists(settings.MEDIA_ROOT):
            os.rmdir(settings.MEDIA_ROOT)
        queryset = event_model.objects.all()
        file_url = generate_csv_from_queryset(queryset)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        assert os.path.exists(file_root)
        os.remove(file_root)

    def test_generate_csv_from_queryset(self, event_model):
        queryset = event_model.objects.all()
        file_url = generate_csv_from_queryset(queryset)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        assert os.path.exists(file_root)
        os.remove(file_root)

    def test_generate_csv_from_queryset_file_name(self, event_model):
        queryset = event_model.objects.all()
        file_url = generate_csv_from_queryset(queryset)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        model_name = queryset.model._meta.model_name
        timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
        expected_file_name = f"{model_name}_{timestamp}.csv"
        assert file_url.split("/")[-1] == expected_file_name
        os.remove(file_root)

    def test_generate_csv_from_queryset_content(self, event_model):
        queryset = event_model.objects.all()
        file_url = generate_csv_from_queryset(queryset)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        with open(file_root, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                assert row
        os.remove(file_root)

    def test_generate_csv_from_serialized_data_without_media_root_folder(self):
        if os.path.exists(settings.MEDIA_ROOT):
            os.rmdir(settings.MEDIA_ROOT)
        data = [
            {"col1": "v1_1", "col2": "v1_2"},
            {"col1": "v1_2", "col2": "v2_2"},
        ]
        file_url = generate_csv_from_serialized_data("test", data)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        assert os.path.exists(file_root)
        os.remove(file_root)

    def test_generate_csv_from_serialized_data(self):
        data = [
            {"col1": "v1_1", "col2": "v1_2"},
            {"col1": "v1_2", "col2": "v2_2"},
        ]
        file_url = generate_csv_from_serialized_data("test", data)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        with open(file_root, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                assert row
        os.remove(file_root)

    def test_generate_csv_from_serialized_data_file_name(self):
        data = [
            {"col1": "v1_1", "col2": "v1_2"},
            {"col1": "v1_2", "col2": "v2_2"},
        ]
        file_url = generate_csv_from_serialized_data("test", data)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
        expected_file_name = f"test_{timestamp}.csv"
        assert file_url.split("/")[-1] == expected_file_name
        os.remove(file_root)

    def test_generate_csv_from_serializer_data_content(self):
        # Test if the file contains the correct data
        data = [
            {"col1": "v1_1", "col2": "v1_2"},
            {"col1": "v1_2", "col2": "v2_2"},
        ]
        file_url = generate_csv_from_serialized_data("test", data)
        file_root = os.path.join(settings.MEDIA_ROOT, file_url.split("/")[-1])
        with open(file_root, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                assert row
        os.remove(file_root)
