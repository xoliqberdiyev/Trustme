from django.contrib import admin

from core.apps.accounts.models.verification_code import VerificationCode

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'code', 'is_expired', 'is_verify']
    