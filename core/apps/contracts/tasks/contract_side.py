from django.contrib.auth import get_user_model

from celery import shared_task

from core.apps.contracts.models.contract import ContractSide, Contract, ContractSignature
from core.services.sms_via_bot import send_sms_code


@shared_task
def create_contract_side(data):
    User = get_user_model()

    contract = Contract.objects.get(id=data['contract_id'])
    user = User.objects.get(phone=data['phone'])

    contract_side = ContractSide.objects.create(
        full_name=data.get('full_name'),
        indentification=data.get('indentification'),
        position=data.get('position'),
        has_indentification=data.get('has_indentification'),
        user_role=data.get('user_role'),
        contract=contract,
        user=user
    )

    ContractSignature.objects.create(
        contract=contract,
        contract_side=contract_side,
    )


