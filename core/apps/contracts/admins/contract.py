from django.contrib import admin

from core.apps.contracts.models.contract import Contract, ContractSide, ContractSignature, ContractSignatureCode


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract_number', 'name', 'face_id', 'attach_file', 'add_folder', 'add_notification']


@admin.register(ContractSide)
class ContractSideAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']


@admin.register(ContractSignature)
class ContractSignatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract_side', 'contract', 'status']


@admin.register(ContractSignatureCode)
class ContractSignatureCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'signature']