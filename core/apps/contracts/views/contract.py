from django.shortcuts import get_object_or_404

from rest_framework import generics, views, status, permissions, parsers
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

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
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Contract.objects.filter(contract_sides__user=self.request.user)


class ContractDetailApiView(views.APIView):
    def get(self, request, id):
        contract = Contract.objects.filter(id=id, contract_sides__user=request.user).prefetch_related('contract_sides').first()
        if not contract:
            return error_message("Contract not found", 404)
        serializer = contract_serializer.ContractDetailSerializer(contract)
        return Response(serializer.data, status=200)
    

class ContractUpdateApiView(generics.GenericAPIView):
    serializer_class = contract_serializer.ContractUpdateSerializer
    queryset = Contract.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        contract = get_object_or_404(Contract, id=id)
        serializer = self.serializer_class(data=request.data, instance=contract)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": True, 'message': 'updated'}, status=200)
        return Response({'success': False, 'message': serializer.errors}, status=400)


class ContractDeleteApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        contract = get_object_or_404(Contract, id=id)
        contract.delete()
        return Response({'success': True, 'message': "deleted"}, status=204)