from django.shortcuts import get_object_or_404

from celery import shared_task

from core.apps.contracts.models.contract import ContractSignature, ContractSignatureCode
from core.services.sms_via_bot import send_sms_code


@shared_task
def send_contract_signature_code(signature_id):
    contract_signature = get_object_or_404(ContractSignature, id=signature_id)
    code = contract_signature.generate_code()
    send_sms_code(code, 'contract', contract_signature.contract_side.user.phone)
        