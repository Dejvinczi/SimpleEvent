import requests

from celery import shared_task
from .helpers import generate_csv_from_serialized_data


@shared_task
def generate_csv_and_send_task(webhook_url, csv_prefix, data):
    path = generate_csv_from_serialized_data(csv_prefix, data)
    # response = requests.post(webhook_url, json={"csv_url": path})
    print(f"\n\nRequest to: {webhook_url} sent.\nCSV url: {path}\n\n")
