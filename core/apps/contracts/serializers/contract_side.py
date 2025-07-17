from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.apps.contracts.models.contract import ContractSide, Contract, ContractSignature
from core.apps.contracts.enums.contract_side import ROLE
from core.apps.contracts.serializers.contract_signature import ContractSignatureListSerializer

User = get_user_model()

class ContractSideCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    indentification = serializers.CharField()
    position = serializers.CharField(required=False)
    has_indentification = serializers.BooleanField()
    user_role = serializers.ChoiceField(choices=ROLE)
    phone = serializers.CharField()
    contract_id = serializers.UUIDField()

    def validate(self, data):
        if not User.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError({'detail': "User not found!"})
        if not Contract.objects.filter(id=data.get('contract_id')).exists():
            raise serializers.ValidationError({'detail': 'Contract not found!'})
        return data
    

class ContractSideListSerializer(serializers.ModelSerializer):
    contract_signature = serializers.SerializerMethodField(method_name='get_contract_signature')

    class Meta:
        model = ContractSide
        fields = [
            'id', 'full_name', 'user', 'contract_signature'
        ]

    def get_contract_signature(self, obj):
        contract_signature = obj.contract_signatures
        return ContractSignatureListSerializer(contract_signature).data 