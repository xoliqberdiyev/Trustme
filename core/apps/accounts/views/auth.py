from django.contrib.auth import get_user_model

from rest_framework import generics, status, views
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from core.apps.accounts.serializers import auth as auth_serializer

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
        

@extend_schema(tags=['auth'])
class RegisterApiView(generics.CreateAPIView):
    serializer_class = auth_serializer.RegisterSerializer
    queryset = User.objects.all()
    permission_classes = []