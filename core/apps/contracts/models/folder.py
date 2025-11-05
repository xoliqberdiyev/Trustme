from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.accounts.models import User


class Folder(BaseModel):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders', null=True  )

    def __str__(self):
        return f"{self.name} folder {self.user.username}"

    class Meta:
        verbose_name = "Fayl"
        verbose_name_plural = "Fayllar"
