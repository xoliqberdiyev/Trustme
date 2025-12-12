from django.db import transaction

from rest_framework import serializers

from core.apps.contracts.models.contract import Contract, Folder
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
    folder_id = serializers.UUIDField(required=False)

    def validate(self, data):
        if data.get('folder_id'):
            folder = Folder.objects.filter(id=data.get('folder_id')).first()
            if not folder:
                raise serializers.ValidationError("Folder not found")
            data['folder'] = folder
        return data

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
                company=user,
                folder=validated_data.get('folder'),
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
            'id', 'name', 'file', 'status', 'contract_number', 'contract_sides',
        ]


class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['folder']

    def update(self, instance, validated_data):
        instance.folder = validated_data.get('folder', instance.folder)
        instance.save()
        return instance