from django.contrib import admin

from core.apps.contracts.models.contract import Contract, ContractFile, ContractNotification,ContractSide, ContractSignature


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract_number', 'name', 'face_id', 'attach_file', 'add_folder', 'add_notification']

@admin.register(ContractSide)
class ContractSideAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']

@admin.register(ContractFile)
class ContractFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ContractNotification)
class ContractNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'contract']

@admin.register(ContractSignature)
class ContractSignatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contract', 'status']