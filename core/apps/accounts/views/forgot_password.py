from rest_framework import generics
from rest_framework.response import Response

from core.apps.accounts.serializers import forgot_password as serializers
from core.apps.accounts.tasks.user import create_and_send_sms_code


class SendCodeApiView(generics.GenericAPIView):
    serializer_class = serializers.SendCodeSerializer
    queryset = None
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            create_and_send_sms_code.delay(data["phone"], "forgot password")
            return Response({"success": True, "message": "Kod yuborildi"}, status=201)
        return Response({"success": False, "message": "Kod yuborilmadi"}, status=400)


class ConfirmCodeApiView(generics.GenericAPIView):
    serializer_class = serializers.ConfirmPasswordSerializer
    queryset = None
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            confirmation = data.get('confirmation')
            if confirmation:
                confirmation.is_verify = True
                confirmation.save()
            return Response({"success": True, "message": "tasdiqlandi"})
        return Response({"success": True, "message": serializer.errors})


class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    queryset = None
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": True, "message": "ozgartirildi"})
        return Response({"success": True, "message": serializer.errors})
