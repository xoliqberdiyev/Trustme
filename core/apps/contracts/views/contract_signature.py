from rest_framework import generics, status, permissions, views
from rest_framework.response import Response

from core.apps.contracts.models.contract import ContractSignature, ContractSignatureCode
from core.apps.contracts.serializers.contract_signature import ContractSignatureSerializer
from core.apps.contracts.tasks.contract_signature import send_contract_signature_code


class SendContractSignatureCodeApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]    
    
    def get(self, request, signature_id):
        # TODO: create and send code with celery in backgroud
        send_contract_signature_code.delay(signature_id)
        return Response({"success": True, "message": "code send"}, status=status.HTTP_200_OK)


class SigningContractApiView(generics.GenericAPIView):
    serializer_class = ContractSignatureSerializer
    queryset = ContractSignature.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        if serializer.is_valid():
            data = serializer.validated_data
            contract = data.get('contract')
            contract_signature = data.get('contract_signature')
            if contract.company == user:
                if contract.status == 'created':
                    contract.status = 'signed_company'
                elif contract.status == 'signed_customer':
                    contract.status = 'signed_contract'
            else:
                if contract.status == 'created':
                    contract.status = 'signed_customer'
                elif contract.status == 'signed_company':
                    contract.status = 'signed_contract'
            contract_signature.status = 'signed'
            contract_signature.save()
            contract.save()
            return Response({'success': True, 'message': 'contract is signed'}, status=status.HTTP_200_OK) 
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)