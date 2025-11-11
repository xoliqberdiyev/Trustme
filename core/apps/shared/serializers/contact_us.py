from rest_framework import serializers

from core.apps.shared.models.contact_us import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'