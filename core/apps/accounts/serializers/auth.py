from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.apps.accounts.tasks.user import create_and_send_sms_code
from core.apps.accounts.enums.user import ROLE_CHOICES

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(phone=data.get('phone'))
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User not found'})
        else:
            if not user.check_password(data.get('password')):
                raise serializers.ValidationError({'detail': 'User not found'})
        data['user'] = user
        return data
    

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError({'detail': "User with this phone number already exists"})
        return data

    def create(self, validated_data):
        with transaction.atomic():
            new_user = User.objects.create_user(
                phone=validated_data.pop('phone'),
                is_active=False
            )
            new_user.set_password(validated_data.pop('password'))
            new_user.save()
            create_and_send_sms_code.delay(new_user.id)
            return new_user

        
class ConfirmUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.IntegerField()

    def validate(self, data):
        try:
            user = User.objects.get(phone=data.get('phone'))
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found"})
        if user.is_active:
            raise serializers.ValidationError({"detail": "User already activated"})
        data['user'] = user
        return data
    

class ChoiseRoleSerializer(serializers.Serializer):
    phone = serializers.CharField()
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    def validate(self, data):
        try:
            user = User.objects.get(phone=data.get("phone"), is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "user not found"})
        data['user'] = user
        return data


class CompliteUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        user = User.objects.filter(email=data.get('email')).first()
        if user:
            raise serializers.ValidationError({'detail': "User with this email already exists"})
        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.first_name = validated_data.get('first_name')
            instance.last_name = validated_data.get('last_name')
            instance.email = validated_data.get('email')
            instance.save()
            return instance