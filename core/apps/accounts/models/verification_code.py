from django.db import models 

from core.apps.shared.models.base import BaseModel
from core.apps.accounts.validators.user import phone_regex


class VerificationCode(BaseModel):
    code = models.PositiveIntegerField()
    phone = models.CharField(max_length=13, validators=[phone_regex])
    is_expired = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    expiration_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.phone} - {self.code}'

    class Meta:
        verbose_name = 'Verification Code'
        verbose_name_plural = 'Verification Codes'
        db_table = 'verification_codes'