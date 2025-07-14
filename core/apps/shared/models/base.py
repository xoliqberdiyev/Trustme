import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True