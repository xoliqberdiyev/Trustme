import random, json, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from core.apps.accounts.managers.user import BaseUserManager
from core.apps.accounts.enums.user import ROLE_CHOICES
from core.apps.accounts.validators.user import phone_regex
from core.apps.accounts.models.verification_code import VerificationCode
from core.apps.shared.models.base import BaseModel


class User(BaseModel, AbstractUser):
    phone = models.CharField(max_length=13, validators=[phone_regex], unique=True)    
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)    
    indentification_num = models.CharField(max_length=14, null=True, blank=True)
    profile_image = models.ImageField(upload_to='users/profile_image/%Y/%m/', null=True, blank=True)

    objects = BaseUserManager()
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
    
    def generate_code(self):
        code = ''.join([str(random.randint(1, 100) % 10) for _ in range(4)])
        expiration_time = timezone.now() + datetime.timedelta(minutes=2)
        VerificationCode.objects.create(
            code=code,
            user=self,
            expiration_time=expiration_time,
        )
        return code

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'