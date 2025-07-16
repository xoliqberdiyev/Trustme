from rest_framework import generics, status, parsers
from rest_framework.response import Response

from core.apps.contracts.serializers import contract_side as contract_side_serializer
from core.apps.contracts.models.contract import ContractSide
from core.apps.contracts.tasks.contract_side import create_contract_side


class ConstartSideCreateApiView(generics.GenericAPIView):
    serializer_class = contract_side_serializer.ContractSideCreateSerializer
    queryset = ContractSide.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # TODO: call celery task
            create_contract_side.delay(serializer.validated_data)
            return Response({"success": True, "message": "contract side created"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
