from django.db import transaction

from rest_framework import generics, status, parsers
from rest_framework.response import Response

from core.apps.contracts.serializers import contract_side as contract_side_serializer
from core.apps.contracts.models.contract import ContractSide, Contract
from core.apps.contracts.tasks.contract_side import create_contract_side
from core.apps.shared.utils.response import error_message, success_message
from core.apps.accounts.models import User

class ContractSideCreateApiView(generics.GenericAPIView):
    serializer_class = contract_side_serializer.ContractSideListCreateSerializer
    queryset = ContractSide.objects.all()

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    for side_data in serializer.validated_data['contract_side']:
                        user = User.objects.get(phone=side_data['phone'])
                        contract = Contract.objects.get(id=side_data['contract_id'])
                        ContractSide.objects.create(
                            full_name=side_data['full_name'],
                            indentification=side_data['indentification'],
                            position=side_data.get('position', ''),
                            has_indentification=side_data['has_indentification'],
                            user_role=side_data['user_role'],
                            # phone=side_data['phone'],
                            contract=contract,
                            user=user
                        )
                return success_message("Contract side created", 201)

            except Exception as e:
                transaction.set_rollback(True)
                return error_message(str(e), 400)

        return error_message(serializer.errors, 400)