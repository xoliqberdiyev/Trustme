from django.conf import settings
from config.env import env

CELERY_BROKER_URL = env.str('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = settings.TIME_ZONE
