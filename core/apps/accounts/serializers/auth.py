from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers

from core.apps.accounts.tasks.user import create_and_send_sms_code
from core.apps.accounts.enums.user import ROLE_CHOICES
from core.apps.accounts.models.verification_code import VerificationCode

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(phone=data.get('phone'))
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User not found'})
        if not user.check_password(data.get('password')):
            raise serializers.ValidationError({'detail': 'User not found, password'})
        data['user'] = user
        return data
    

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User exists with this phone")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User exists with this email")        
        return value


class ConfirmUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.IntegerField()

    def validate(self, data):
        phone = data['phone']
        code = data['code']
        confirmation = VerificationCode.objects.filter(code=code, phone=phone).first()
        if confirmation and confirmation.is_verify:
            raise serializers.ValidationError("Code is verified")
        if confirmation: 
            if confirmation.is_expired or confirmation.expiration_time < timezone.now().time():
                raise serializers.ValidationError("Code is expired")
            data['confirmation'] = confirmation        
        return data
    

class ChoiseRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)


class UserPhoneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone']