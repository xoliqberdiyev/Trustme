from celery import shared_task

from core.apps.accounts.models.verification_code import VerificationCode
from core.services.sms import send_sms_eskiz

@shared_task
def create_and_send_sms_code(user):
    code = user.generate_code()
    send_sms_eskiz(user.phone, code)