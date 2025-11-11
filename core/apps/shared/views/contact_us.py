from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.apps.shared.utils.response import success_message, error_message
from core.apps.shared.serializers.contact_us import ContactUsSerializer
from core.apps.shared.models import ContactUs


class ContactUsApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ContactUs.objects.first()
    serializer_class = ContactUsSerializer

    def get(self, request):
        obj = ContactUs.objects.first()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=200)
