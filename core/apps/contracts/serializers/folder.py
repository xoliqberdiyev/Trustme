from rest_framework import serializers

from core.apps.contracts.models import Folder


class FolderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = [
            'id', 'name'
        ]


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = [
            'name'
        ]

    def create(self, validated_data):
        folder = Folder.objects.create(
            name=validated_data.get('name'),
            user=self.context.get('user'),
        )
        return folder

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance