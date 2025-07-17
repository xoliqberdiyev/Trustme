from celery import shared_task

from core.apps.accounts.models.verification_code import VerificationCode
from core.apps.accounts.models.user import User
from core.services.sms import send_sms_eskiz
from core.services.sms_via_bot import send_sms_code

@shared_task
def create_and_send_sms_code(user):
    user = User.objects.get(id=user)
    code = user.generate_code()
    # send_sms_eskiz(user.phone, code)
    send_sms_code(code, 'auth', user.phone)
