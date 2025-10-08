import os

import celery

from config.env import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

app = celery.Celery('config', broker="redis://redis:6379", backend="redis://redis:6379")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()