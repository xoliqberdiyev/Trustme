import pytest
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient

from core.apps.accounts.models.verification_code import VerificationCode


@pytest.mark.django_db
class TestLoginAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.password = '20090912'
        self.phone = '+998947099971'
        self.user = get_user_model().objects.create_user(
            phone=self.phone, password=self.password            
        )
        self.new_user_phone = '+998947099972'
        self.new_user = get_user_model().objects.create_user(
            phone=self.new_user_phone, password=self.password, is_active=False           
        )

    def test_login_success(self):
        url = reverse('login')
        response = self.client.post(url, {
            "phone": self.phone,
            "password": self.password
        })

        assert response.status_code == 200 
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data
        assert 'role' in response.data

    def test_login_user_not_found(self):
        url = reverse('login')
        response = self.client.post(url, {
            'phone': self.phone,
            'password': 'somepass'
        })
        assert response.status_code == 400
        assert 'detail' in response.data
    
    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, {
            'phone': '+998947099973',
            'password': self.password
        })

        assert response.status_code == 200
    
    def test_register_user_exists(self):
        url = reverse('register')
        response = self.client.post(url, {
            'phone': '+998947099971',
            'password': self.password
        })

        assert response.status_code == 400

    
    def test_confirm_user_is_active(self):
        time = timezone.now() + timedelta(minutes=2)
        code = VerificationCode.objects.create(phone=self.phone, code=1111, expiration_time=time)
        url = reverse('confirm-user')
        response = self.client.post(url, {
            'phone': self.phone,
            'code': code.code
        })

        assert response.status_code == 404
        assert 'message' in response.data
        assert 'success' in response.data

    def test_confirm_user_code_is_expired(self):
        time = timezone.now()
        code = VerificationCode.objects.create(
            phone=self.new_user_phone, code=1111, expiration_time=time
        )
        url = reverse('confirm-user')
        response = self.client.post(url, {
            'phone': self.new_user_phone,
            'code': code.code
        })

        assert response.status_code == 400
        assert 'message' in response.data
        assert 'success' in response.data
    
    def test_confirm_user_code_is_verify(self):
        time = timezone.now() + timedelta(minutes=2)
        code = VerificationCode.objects.create(
            phone=self.new_user_phone, code=1111, expiration_time=time, is_verify=True
        )
        url = reverse('confirm-user')
        response = self.client.post(url, {
            'phone': self.new_user_phone,
            'code': code.code
        })

        assert response.status_code == 400
        assert 'message' in response.data
        assert 'success' in response.data
    
    def test_confirm_user_serializer_error(self):
        time = timezone.now() + timedelta(minutes=2)
        code = VerificationCode.objects.create(
            phone=self.phone, code=1111, expiration_time=time, is_verify=True
        )
        url = reverse('confirm-user')
        response = self.client.post(url, {
            'code': code.code
        })
        assert response.status_code == 400
        assert 'message' in response.data
        assert response.data['message']['phone'][0] == "Ushbu maydon to'ldirilishi shart."
        assert 'success' in response.data
    
    def test_choice_user_role_success(self):
        url = reverse('choise-user-role')
        self.client.login(phone=self.phone, password=self.password)
        response = self.client.post(url, {
            'role': 'LP',
        })

        assert response.status_code == 200
        assert response.data['success'] == True

    def test_choice_user_role_wrong_choice(self):
        url = reverse('choise-user-role')
        self.client.login(phone=self.phone, password=self.password)
        response = self.client.post(url, {
            'phone': self.new_user,
            'role': 'LL',
        })
        assert response.status_code == 400
        assert response.data['success'] == False
        assert response.data['message']['role'][0] == '"LL" is not a valid choice.'
    
    def test_complite_user_profile_success(self):
        url = reverse('complite-user-profile')
        self.client.login(phone=self.phone, password=self.password)
        response = self.client.put(url, data={
            'first_name': 'behruz',
            'last_name': 'xoliqberdiyev',
            'email': 'xoliqberdiyev@gmail.com'
        })  

        assert response.status_code == 200
        assert 'success' in response.data
        assert 'message' in response.data