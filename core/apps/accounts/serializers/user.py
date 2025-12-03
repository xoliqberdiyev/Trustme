from rest_framework import serializers

from core.apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'phone', 'indentification_num', 'profile_image', 'first_name', 'last_name', 'email', 'role'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'indentification_num', 'profile_image', 'first_name', 'last_name', 'email'
        ]
    
    def update(self, instance, validated_data):
        instance.indentification_num = validated_data.get('indentification_num', instance.indentification_num)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance