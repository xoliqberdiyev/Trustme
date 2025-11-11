from django.db import models

from core.apps.shared.models.base import BaseModel


class ContactUs(BaseModel):
    phone_number = models.CharField(max_length=20)
    telegram_url = models.URLField()

    def __str__(self):
        return self.phone_number
    