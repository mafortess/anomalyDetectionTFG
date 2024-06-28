from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .views import collect_data, detect_anomalies

@shared_task
def collect_and_detect_anomalies():
    collect_data()
    detect_anomalies()
