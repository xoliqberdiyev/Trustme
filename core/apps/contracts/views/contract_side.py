from rest_framework import generics, status, parsers
from rest_framework.response import Response

from core.apps.contracts.serializers import contract_side as contract_side_serializer
from core.apps.contracts.models.contract import ContractSide
from core.apps.contracts.tasks.contract_side import create_contract_side
from core.apps.shared.utils.response import error_message, success_message

class ConstartSideCreateApiView(generics.GenericAPIView):
    serializer_class = contract_side_serializer.ContractSideCreateSerializer
    queryset = ContractSide.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # TODO: call celery task
            create_contract_side.delay(serializer.validated_data)
            return success_message("Contract side created", 201)
        return error_message(serializer.error_messages, 400)
    
