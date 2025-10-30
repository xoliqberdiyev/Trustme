from django.utils import timezone

from rest_framework import serializers

from core.apps.accounts.models import User, VerificationCode


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            raise serializers.ValidationError("User not found")
        data['user'] = user
        data['phone'] = user.phone
        return data


class   ConfirmPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    phone = serializers.CharField()

    def validate(self, data):
        phone = data["phone"]
        code = data["code"]
        confirmation = VerificationCode.objects.filter(code=code, phone=phone).first()
        if confirmation and confirmation.is_verify:
            raise serializers.ValidationError("Code is verified")
        if confirmation:
            if (
                confirmation.is_expired
                or confirmation.expiration_time < timezone.now().time()
            ):
                raise serializers.ValidationError("Code is expired")
            data["confirmation"] = confirmation
        return data


class ResetPasswordSerializer(serializers.Serializer): 
    phone = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            raise serializers
        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data.get('user')
        user.set_password(self.validated_data.get('new_password'))
        user.save()
        return super().save(**kwargs)