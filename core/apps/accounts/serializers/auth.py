from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers

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
            )
            new_user.set_password(validated_data.pop('password'))
            new_user.save()
            return new_user

        
