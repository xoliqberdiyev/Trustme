from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import generics, status, views
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from core.apps.accounts.serializers import auth as auth_serializer
from core.apps.accounts.models.verification_code import VerificationCode

User = get_user_model()

@extend_schema(tags=['auth'])
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
        

@extend_schema(tags=['auth'])
class RegisterApiView(generics.CreateAPIView):
    serializer_class = auth_serializer.RegisterSerializer
    queryset = User.objects.all()
    permission_classes = []


@extend_schema(tags=['auth'])
class ConfirUserApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.ConfirmUserSerializer
    queryset = User.objects.all()
    permission_classes = []
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            code = serializer.validated_data.get('code')
            code = VerificationCode.objects.filter(user=user, code=code).first()
            if code:
                if code.is_expired or code.expiration_time < timezone.now().time():
                    return Response({"success": True, "message": "code is expired"}, status=status.HTTP_400_BAD_REQUEST)
                if code.is_verify:
                    return Response({"success": True, "message": "code is verified"}, status=status.HTTP_400_BAD_REQUEST)
                user.save()
                code.is_verify = True
                code.is_expired = True
                code.save()
                return Response({"success": True, "message": "user activated"}, status=status.HTTP_202_ACCEPTED) 
            return Response({"success": False, "message": "code is wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'])
class ChoiceUserRoleApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.ChoiseRoleSerializer
    queryset = User.objects.all()
    permission_classes = []

    @extend_schema(description="roles -> PP(physcal person) or LP(legal person)")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            role = serializer.validated_data.get('role')
            user.role = role
            user.save()
            return Response({'success': True, 'message': "role is selected"}, status=status.HTTP_200_OK)
        return Response({'success': False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'])
class CompliteUserProfileApiView(generics.GenericAPIView):
    serializer_class = auth_serializer.CompliteUserProfileSerializer
    queryset = User.objects.all()
    permission_classes = []

    def put(self, request, phone):
        user = User.objects.filter(phone=phone, is_active=True).first()
        if user:
            serializer = self.serializer_class(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                token = RefreshToken.for_user(user)
                return Response({'access_token': str(token.access_token), "refresh_token": str(token), "role": user.role}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
