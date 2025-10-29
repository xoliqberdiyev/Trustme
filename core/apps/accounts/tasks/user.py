import random
from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from core.apps.accounts.models.verification_code import VerificationCode
from core.apps.accounts.models.user import User
from core.services.sms import send_sms_eskiz
from core.services.sms_via_bot import send_sms_code

@shared_task
def create_and_send_sms_code(phone, type):
    verification = VerificationCode.objects.create(
        code=''.join([str(random.randint(1, 100) % 10) for _ in range(4)]),
        phone=phone,
        expiration_time=timezone.now() + timedelta(minutes=2)
    )
    # send_sms_eskiz(user.phone, code)
    send_sms_code(verification.code, type, verification.phone)
