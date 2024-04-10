"""Core module helpers."""

import os
import csv

from django.utils import timezone
from django.conf import settings


def generate_csv_from_queryset(queryset):
    """
    Create CSV file from queryset.

    This function generates a CSV file with the data from the queryset.
    The file is saved in the MEDIA_ROOT directory with a timestamp in its name.

    Args:
        queryset (QuerySet): A Django queryset to generate CSV from.

    Returns:
        str: Path to the generated CSV file.
    """
    timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    model_name = queryset.model._meta.model_name
    file_name = f"{model_name}_{timestamp}.csv"
    file_root = os.path.join(settings.MEDIA_ROOT, file_name)
    file_url = os.path.join(settings.MEDIA_URL, file_name)
    field_names = [field.name for field in queryset.model._meta.concrete_fields]

    if not os.path.exists(settings.MEDIA_ROOT):
        os.mkdir(settings.MEDIA_ROOT)

    with open(file_root, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        data = queryset.values(*field_names)
        writer.writerows(data)

    return file_url


def generate_csv_from_serialized_data(prefix, data):
    """
    Generate a CSV file from serialized data.

    Args:
        prefix (str): The prefix for the file name.
        data (list): A list of dictionaries containing the serialized data.

    Returns:
        str: The file url of the generated CSV file.
    """
    timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{prefix}_{timestamp}.csv"
    file_root = os.path.join(settings.MEDIA_ROOT, file_name)
    file_url = os.path.join(settings.MEDIA_URL, file_name)
    field_names = data[0].keys() if len(data) else []

    if not os.path.exists(settings.MEDIA_ROOT):
        os.mkdir(settings.MEDIA_ROOT)

    with open(file_root, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)

    return file_url
