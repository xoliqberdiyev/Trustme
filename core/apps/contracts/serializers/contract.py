from django.db import transaction

from rest_framework import serializers

from core.apps.contracts.models.contract import Contract
from core.apps.contracts.serializers.contract_side import ContractSideCreateSerializer, ContractSideListSerializer


class ContractCreateSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)
    contract_number = serializers.IntegerField()
    name = serializers.CharField()    
    sides = serializers.ChoiceField(choices=('two_or_more', 'customer_only', 'only_company'))
    face_id = serializers.BooleanField()
    attach_file = serializers.BooleanField()
    add_folder = serializers.BooleanField() 
    add_notification = serializers.BooleanField()

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context.get('user')
            contract = Contract.objects.create(
                file=validated_data.pop('file'),
                contract_number=validated_data.pop('contract_number'),
                name=validated_data.pop('name'),
                sides=validated_data.pop('sides'),
                face_id=validated_data.pop('face_id'),
                attach_file=validated_data.pop('attach_file'),
                add_folder=validated_data.pop('add_folder'),
                add_notification=validated_data.pop('add_notification'),
                company=user
            )
            return contract.id


class ContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract 
        fields = [
            'id', 'name', 'file', 'contract_number', 'sides', 'face_id', 'add_folder', 'attach_file', 'add_notification', 'created_at'
        ]


class ContractDetailSerializer(serializers.ModelSerializer):
    contract_sides = ContractSideListSerializer(many=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'name', 'file', 'contract_number', 'contract_sides',
        ]