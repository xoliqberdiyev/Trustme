from rest_framework import generics, views, status, permissions, parsers
from rest_framework.response import Response

from core.apps.contracts.serializers import contract as contract_serializer
from core.apps.contracts.models.contract import Contract
from core.apps.shared.utils.response import success_message, error_message



class ContractCreateApiView(generics.CreateAPIView):
    serializer_class = contract_serializer.ContractCreateSerializer
    queryset = Contract.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] 
    
    def get_serializer_context(self):
        return {'user': self.request.user}
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.save()
        return success_message(str(contract), 201)


class ContractListApiView(generics.ListAPIView):
    serializer_class = contract_serializer.ContractListSerializer
    queryset = Contract.objects.all()

    def get_queryset(self):
        return Contract.objects.filter(contract_sides__user=self.request.user)


class ContractDetailApiView(views.APIView):
    def get(self, request, id):
        contract = Contract.objects.filter(id=id, contract_sides__user=request.user).prefetch_related('contract_sides').first()
        if not contract:
            return error_message("Contract not found", 404)
        serializer = contract_serializer.ContractDetailSerializer(contract)
        return Response(serializer.data, status=200)    