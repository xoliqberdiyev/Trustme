from django.db import models 

from core.apps.shared.models.base import BaseModel

class VerificationCode(BaseModel):
    code = models.PositiveIntegerField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='verification_codes')
    is_expired = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    expiration_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.phone} - {self.code}'

    class Meta:
        verbose_name = 'Verification Code'
        verbose_name_plural = 'Verification Codes'
        db_table = 'verification_codes'