from django.db import models

from core.apps.shared.models.base import BaseModel


class Folder(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'folder'
        verbose_name_plural = 'folders'
        db_table = 'folders'
