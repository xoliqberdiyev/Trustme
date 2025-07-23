import pytest, os
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from rest_framework.test import APIClient

from core.apps.contracts.models.contract import Contract, ContractSide, ContractSignature, ContractSignatureCode


@pytest.mark.django_db
class TestContractApi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()   
        self.password = '20090912'
        self.phone = '+998947099971'
        self.user = get_user_model().objects.create_user(
            phone=self.phone, password=self.password            
        )

    def test_contract_create(self):
        url = reverse('create-contract')
        self.client.login(phone=self.phone, password=self.password)
        fake_image = SimpleUploadedFile("test.avif", b"file_content", content_type="image/avif")
        data = {
            'file': fake_image,
            'contract_number': 1,
            'name': 'test name',
            'sides': 'two_or_more',
            'face_id': True,
            'attach_file': True,
            'add_folder': False,
            'add_notification': True,   
        }
        response = self.client.post(url, data=data, format='multipart')

        assert response.status_code == 201

    def test_contract_list(self):
        url = reverse('list-contract')
        self.client.login(phone=self.phone, password=self.password)
        
        response = self.client.get(url)

        assert response.status_code == 200

    def test_contract_detail(self):
        fake_image = SimpleUploadedFile("test.avif", b"file_content", content_type="image/avif")

        contract = Contract.objects.create(
            file=fake_image,
            contract_number=1,
            name='test',
            sides='two_or_more',
            status='created',
            company=self.user
        )
        contract_side = ContractSide.objects.create(
            contract=contract, 
            user=self.user,
            user_role='legal',
            full_name='salom',
            indentification='ssss',
        )
        contract_signature = ContractSignature.objects.create(
            contract=contract,
            contract_side=contract_side
        )
        url = reverse('detail-contract', kwargs={'id': contract.id})
        self.client.force_login(self.user)
        response = self.client.get(url)

        assert response.status_code == 200
    
@pytest.mark.django_db
class TestContractSideApi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()   
        self.password = '20090912'
        self.phone = '+998947099971'
        self.user = get_user_model().objects.create_user(
            phone=self.phone, password=self.password            
        )

    def test_contract_side_create(self):
        fake_image = SimpleUploadedFile("test.avif", b"file_content", content_type="image/avif")

        contract = Contract.objects.create(
            file=fake_image,
            contract_number=1,
            name='test',
            sides='two_or_more',
            status='created',
            company=self.user
        )
        self.client.force_login(self.user)
        data = {
            "full_name": "string",
            "indentification": "string",
            "position": "string",
            "has_indentification": True,
            "user_role": "physical",
            "phone": "+998947099971",
            "contract_id": contract.id
        }

        url = reverse('contract-side-create')
        response = self.client.post(url, data=data)
        print(response.data)
        assert response.status_code == 201


@pytest.mark.django_db
class TestContractSignatureApi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()   
        self.password = '20090912'
        self.phone = '+998947099971'
        self.user = get_user_model().objects.create_user(
            phone=self.phone, password=self.password            
        )
        fake_image = SimpleUploadedFile("test.avif", b"file_content", content_type="image/avif")
        self.contract = Contract.objects.create(
            file=fake_image,
            contract_number=1,
            name='test',
            sides='two_or_more',
            status='created',
            company=self.user
        )
        self.client.force_login(self.user)


    def test_send_signature_code(self):
        data = {
            "full_name": "string",
            "indentification": "string",
            "position": "string",
            "has_indentification": True,
            "user_role": "physical",
            "user": self.user,
            "contract_id": self.contract.id
        }
        contract_side = ContractSide.objects.create(**data)
        contract_signature = ContractSignature.objects.create(
            contract=self.contract,
            contract_side=contract_side,
        )
        url = reverse('send-signature-code', kwargs={'signature_id': contract_signature.id})
        response = self.client.get(url)

        assert response.status_code == 200

    def test_confirm_signature_code(self):
        data = {
            "full_name": "string",
            "indentification": "string",
            "position": "string",
            "has_indentification": True,
            "user_role": "physical",
            "user": self.user,
            "contract_id": self.contract.id
        }
        contract_side = ContractSide.objects.create(**data)
        contract_signature = ContractSignature.objects.create(
            contract=self.contract,
            contract_side=contract_side,
        )
        code = ContractSignatureCode.objects.create(
            code=1111,
            signature=contract_signature,
            expiration_time=timezone.now() + timedelta(minutes=2)
        )

        url = reverse('sign-contract')
        response = self.client.post(url, data={
            'code': 1111,
            'signature_id': contract_signature.id
        })

        assert response.status_code == 200