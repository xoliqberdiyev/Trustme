from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import generics, status, views
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.accounts.serializers import auth as auth_serializer
from core.apps.accounts.models.verification_code import VerificationCode
from core.apps.accounts.cache.user import cache_user_credentials, get_user_creadentials
from core.apps.accounts.tasks import user as user_tasks

User = get_user_model()


class LoginApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.LoginSerializer
    queryset = User.objects.all()
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            tokens = RefreshToken.for_user(user)
            return Response({'access_token': str(tokens.access_token), 'refresh_token': str(tokens), 'role': user.role}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        

class RegisterApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.RegisterSerializer
    queryset = None
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            cache_user_credentials(data['phone'], data['password'], 300)
            user_tasks.create_and_send_sms_code.delay(data['phone'])
            return Response(
                {'success': True, "message": "code send"},
                status=status.HTTP_200_OK
            )
        return Response(
            {'success': True, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class ConfirUserApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.ConfirmUserSerializer
    queryset = None
    permission_classes = []
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            confirmation = serializer.validated_data.get('confirmation')
            data = get_user_creadentials(phone)
            if not data:
                return Response(
                    {'success': True, "message": 'not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            user = User.objects.create_user(phone=data['phone'], password=data['password'])
            confirmation.is_verify = True
            confirmation.save()
            token = RefreshToken.for_user(user)
            return Response(
                {"access": str(token.access_token), "refresh": str(token)},
                status=status.HTTP_202_ACCEPTED
            ) 
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChoiceUserRoleApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.ChoiseRoleSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            role = serializer.validated_data.get('role')
            user.role = role
            user.save()
            return Response({'success': True, 'message': "role is selected"}, status=status.HTTP_200_OK)
        return Response({'success': False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CompliteUserProfileApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.CompliteUserProfileSerializer
    queryset = User.objects.all()

    def put(self, request):
        user = request.user
        if user:
            serializer = self.serializer_class(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, "message": "Ok"}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)