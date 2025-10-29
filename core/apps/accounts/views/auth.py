from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.accounts.serializers import auth as auth_serializer
from core.apps.accounts.models.verification_code import VerificationCode
from core.apps.accounts.cache.user import cache_user_credentials, get_user_creadentials
from core.apps.accounts.tasks import user as user_tasks
from core.apps.shared.utils.response import success_message, error_message

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
            cache_user_credentials(
                data['phone'], data['password'], data['first_name'],
                data['last_name'], data['email'], 300
            )
            user_tasks.create_and_send_sms_code.delay(data['phone'], type='auth')
            return success_message("code is send", 200)
        return error_message(serializer.errors, 400)


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
                return error_message("Not found", 404)
            user = User.objects.create_user(
                phone=data['phone'], first_name=data['first_name'],
                last_name=data['last_name'], email=data['email']
            )
            user.set_password(data['password'])
            user.save()
            confirmation.is_verify = True
            confirmation.save()
            token = RefreshToken.for_user(user)
            return Response(
                {"access": str(token.access_token), "refresh": str(token)},
                status=status.HTTP_202_ACCEPTED
            ) 
        return error_message(serializer.errors, 400)


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
            return success_message('role choices', 200)
        return error_message(serializer.errors, 400)
    

class SearchUserPhoneApiView(generics.GenericAPIView):
    serializer_class = None
    queryset = User.objects.all()

    def get(self, request, number):
        users = User.objects.filter(phone__istartswith=number)
        serializer = auth_serializer.UserPhoneListSerializer(users, many=True)
        return Response(serializer.data, status=200)