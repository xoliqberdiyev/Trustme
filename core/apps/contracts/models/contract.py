from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from core.apps.shared.models.base import BaseModel
from core.apps.contracts.enums.contract import SIDES, STATUS
from core.apps.contracts.enums.contract_side import ROLE
from core.apps.contracts.enums.contract_signature import SIGNATURE_TYPE, SIGNATURE_STATUS


class Contract(BaseModel):
    file = models.FileField(upload_to="contract/files/%Y/%m/")
    contract_number = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    
    sides = models.CharField(max_length=13, choices=SIDES) # choices
    status = models.CharField(max_length=15, choices=STATUS, default='created') # choices
 
    face_id = models.BooleanField(default=False)
    attach_file = models.BooleanField(default=False)
    add_folder = models.BooleanField(default=False)
    add_notification = models.BooleanField(default=False)

    company = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='c')

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'
        db_table = 'contracts'


class ContractSide(BaseModel):
    full_name = models.CharField(max_length=70)
    indentification = models.CharField(max_length=20)
    position = models.CharField(max_length=50, null=True, blank=True)

    has_indentification = models.BooleanField(default=False)

    user_role = models.CharField(max_length=9, choices=ROLE)
    
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_sides')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='contract_sides')

    def __str__(self):
        return f"{self.full_name} - {self.contract}"
    
    class Meta:
        verbose_name = 'contract side'
        verbose_name_plural = 'contract sides'
        db_table = 'contracts_sides'
        unique_together = ['contract', 'user']


class ContractSignature(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_signatures')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='contract_users')

    status = models.CharField(max_length=20, choices=SIGNATURE_STATUS, default='organized') 
    signature_type = models.CharField(max_length=20, choices=SIGNATURE_TYPE, null=True, blank=True)

    is_signature = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} user signature for {self.contract} contract'
    
    class Meta:
        verbose_name = 'contract signature'
        verbose_name = 'contract signatures'
        db_table = 'contract_signatures'
        unique_together = ['contract', 'user']
