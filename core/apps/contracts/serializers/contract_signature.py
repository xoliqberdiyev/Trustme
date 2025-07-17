from django.utils import timezone

from rest_framework import serializers

from core.apps.contracts.models.contract import ContractSignature, ContractSignatureCode


class ContractSignatureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractSignature
        fields = [
            'id', 'status', 'signature_type', 'is_signature'
        ]
    

class ContractSignatureSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    signature_id = serializers.UUIDField()

    def validate(self, data):
        user = self.context.get('user')
        signature = ContractSignature.objects.filter(id=data.get('signature_id')).first()
        if not signature:
            raise serializers.ValidationError({"detail": "contract signature not found"})
        if signature.contract_side.user != user:
            raise serializers.ValidationError({'detail': 'this is not your code'})
        signature_code = ContractSignatureCode.objects.filter(signature=signature, code=data.get('code')).first()
        if not signature_code:
            raise serializers.ValidationError({'detail': 'invalid code'})
        if signature_code.expiration_time < timezone.now():
            raise serializers.ValidationError({"detail": 'code is expired'})
        data['contract'] = signature.contract_side.contract
        data['contract_signature'] = signature
        return data
